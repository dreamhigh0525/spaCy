from typing import TYPE_CHECKING, Dict, Any, Tuple, Callable, List, Optional, IO
from wasabi import Printer
import tqdm
import sys

from ..util import registry
from .. import util
from ..errors import Errors

if TYPE_CHECKING:
    from ..language import Language  # noqa: F401


@registry.loggers("spacy.ConsoleLogger.v1")
def console_logger(progress_bar: bool = False):
    def setup_printer(
        nlp: "Language", stdout: IO = sys.stdout, stderr: IO = sys.stderr
    ) -> Tuple[Callable[[Optional[Dict[str, Any]]], None], Callable[[], None]]:
        msg = Printer(no_print=True)
        # we assume here that only components are enabled that should be trained & logged
        logged_pipes = nlp.pipe_names
        eval_frequency = nlp.config["training"]["eval_frequency"]
        score_weights = nlp.config["training"]["score_weights"]
        score_cols = [col for col, value in score_weights.items() if value is not None]
        score_widths = [max(len(col), 6) for col in score_cols]
        loss_cols = [f"Loss {pipe}" for pipe in logged_pipes]
        loss_widths = [max(len(col), 8) for col in loss_cols]
        table_header = ["E", "#"] + loss_cols + score_cols + ["Score"]
        table_header = [col.upper() for col in table_header]
        table_widths = [3, 6] + loss_widths + score_widths + [6]
        table_aligns = ["r" for _ in table_widths]
        stdout.write(msg.row(table_header, widths=table_widths) + "\n")
        stdout.write(msg.row(["-" * width for width in table_widths]) + "\n")
        progress = None

        def log_step(info: Optional[Dict[str, Any]]) -> None:
            nonlocal progress

            if info is None:
                # If we don't have a new checkpoint, just return.
                if progress is not None:
                    progress.update(1)
                return
            losses = [
                "{0:.2f}".format(float(info["losses"][pipe_name]))
                for pipe_name in logged_pipes if pipe_name in info["losses"]
            ]

            scores = []
            for col in score_cols:
                score = info["other_scores"].get(col, 0.0)
                try:
                    score = float(score)
                except TypeError:
                    err = Errors.E916.format(name=col, score_type=type(score))
                    raise ValueError(err) from None
                if col != "speed":
                    score *= 100
                scores.append("{0:.2f}".format(score))

            data = (
                [info["epoch"], info["step"]]
                + losses
                + scores
                + ["{0:.2f}".format(float(info["score"]))]
            )
            if progress is not None:
                progress.close()
            stdout.write(msg.row(data, widths=table_widths, aligns=table_aligns) + "\n")
            if progress_bar:
                # Set disable=None, so that it disables on non-TTY
                progress = tqdm.tqdm(
                    total=eval_frequency, disable=None, leave=False, file=stderr
                )
                progress.set_description(f"Epoch {info['epoch']+1}")

        def finalize() -> None:
            pass

        return log_step, finalize

    return setup_printer


@registry.loggers("spacy.WandbLogger.v1")
def wandb_logger(project_name: str, remove_config_values: List[str] = []):
    import wandb

    console = console_logger(progress_bar=False)

    def setup_logger(
        nlp: "Language", stdout: IO = sys.stdout, stderr: IO = sys.stderr
    ) -> Tuple[Callable[[Dict[str, Any]], None], Callable[[], None]]:
        config = nlp.config.interpolate()
        config_dot = util.dict_to_dot(config)
        for field in remove_config_values:
            del config_dot[field]
        config = util.dot_to_dict(config_dot)
        wandb.init(project=project_name, config=config, reinit=True)
        console_log_step, console_finalize = console(nlp, stdout, stderr)

        def log_step(info: Optional[Dict[str, Any]]):
            console_log_step(info)
            if info is not None:
                score = info["score"]
                other_scores = info["other_scores"]
                losses = info["losses"]
                wandb.log({"score": score})
                if losses:
                    wandb.log({f"loss_{k}": v for k, v in losses.items()})
                if isinstance(other_scores, dict):
                    wandb.log(other_scores)

        def finalize() -> None:
            console_finalize()
            wandb.join()

        return log_step, finalize

    return setup_logger

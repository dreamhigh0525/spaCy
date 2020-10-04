import React from 'react'
import PropTypes from 'prop-types'
import { StaticQuery, graphql } from 'gatsby'

import {
    LandingHeader,
    LandingTitle,
    LandingSubtitle,
    LandingGrid,
    LandingCard,
    LandingCol,
    LandingDemo,
    LandingBannerGrid,
    LandingBanner,
} from '../components/landing'
import { H2 } from '../components/typography'
import { Ul, Li } from '../components/list'
import { InlineCode } from '../components/code'
import Button from '../components/button'
import Link from '../components/link'

import QuickstartTraining from './quickstart-training'
import Project from './project'
import courseImage from '../../docs/images/course.jpg'
import prodigyImage from '../../docs/images/prodigy_overview.jpg'
import projectsImage from '../../docs/images/projects.png'
import irlBackground from '../images/spacy-irl.jpg'

import Benchmarks from 'usage/_benchmarks-models.md'

const CODE_EXAMPLE = `# pip install spacy
# python -m spacy download en_core_web_sm
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = ("When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
`

const Landing = ({ data }) => {
    const { counts } = data
    return (
        <>
            <LandingHeader nightly={data.nightly}>
                <LandingTitle>
                    Industrial-Strength
                    <br />
                    Natural Language
                    <br />
                    Processing
                </LandingTitle>
                <LandingSubtitle>in Python</LandingSubtitle>
            </LandingHeader>
            <LandingGrid blocks>
                <LandingCard title="Get things done" url="/usage/spacy-101" button="Get started">
                    spaCy is designed to help you do real work — to build real products, or gather
                    real insights. The library respects your time, and tries to avoid wasting it.
                    It's easy to install, and its API is simple and productive.
                </LandingCard>
                <LandingCard
                    title="Blazing fast"
                    url="/usage/facts-figures"
                    button="Facts &amp; Figures"
                >
                    spaCy excels at large-scale information extraction tasks. It's written from the
                    ground up in carefully memory-managed Cython. If your application needs to
                    process entire web dumps, spaCy is the library you want to be using.
                </LandingCard>

                <LandingCard title="Awesome ecosystem" url="/usage/projects" button="Read more">
                    In the five years since its release, spaCy has become an industry standard with
                    a huge ecosystem. Choose from a variety of plugins, integrate with your machine
                    learning stack and build custom components and workflows.
                </LandingCard>
            </LandingGrid>

            <LandingGrid>
                <LandingDemo title="Edit the code & try spaCy">{CODE_EXAMPLE}</LandingDemo>

                <LandingCol>
                    <H2>Features</H2>
                    <Ul>
                        <Li>
                            ✅ Support for <strong>{counts.langs}+ languages</strong>
                        </Li>
                        <Li>
                            ✅ <strong>{counts.models} trained pipelines</strong> for{' '}
                            {counts.modelLangs} languages
                        </Li>
                        <Li>
                            ✅ Multi-task learning with pretrained <strong>transformers</strong>{' '}
                            like BERT
                        </Li>
                        <Li>
                            ✅ Pretrained <strong>word vectors</strong>
                        </Li>
                        <Li>✅ State-of-the-art speed</Li>
                        <Li>
                            ✅ Production-ready <strong>training system</strong>
                        </Li>
                        <Li>
                            ✅ Linguistically-motivated <strong>tokenization</strong>
                        </Li>
                        <Li>
                            ✅ Components for <strong>named entity</strong> recognition,
                            part-of-speech tagging, dependency parsing, sentence segmentation,{' '}
                            <strong>text classification</strong>, lemmatization, morphological
                            analysis, entity linking and more
                        </Li>
                        <Li>
                            ✅ Easily extensible with <strong>custom components</strong> and
                            attributes
                        </Li>
                        <Li>
                            ✅ Support for custom models in <strong>PyTorch</strong>,{' '}
                            <strong>TensorFlow</strong> and other frameworks
                        </Li>
                        <Li>
                            ✅ Built in <strong>visualizers</strong> for syntax and NER
                        </Li>
                        <Li>
                            ✅ Easy <strong>model packaging</strong>, deployment and workflow
                            management
                        </Li>
                        <Li>✅ Robust, rigorously evaluated accuracy</Li>
                    </Ul>
                </LandingCol>
            </LandingGrid>

            <LandingBannerGrid>
                <LandingBanner
                    label="New in v3.0"
                    title="Transformer-based pipelines, new training system, project templates &amp; more"
                    to="/usage/v3"
                    button="See what's new"
                    small
                >
                    spaCy v3.0 features all new <strong>transformer-based pipelines</strong> that
                    bring spaCy's accuracy right up to the current <strong>state-of-the-art</strong>
                    . You can use any pretrained transformer to train your own pipelines, and even
                    share one transformer between multiple components with{' '}
                    <strong>multi-task learning</strong>. Training is now fully configurable and
                    extensible, and you can define your own custom models using{' '}
                    <strong>PyTorch</strong>, <strong>TensorFlow</strong> and other frameworks. The
                    new spaCy projects system lets you describe whole{' '}
                    <strong>end-to-end workflows</strong> in a single file, giving you an easy path
                    from prototype to production, and making it easy to clone and adapt
                    best-practice projects for your own use cases.
                </LandingBanner>

                <LandingBanner
                    title="Prodigy: Radically efficient machine teaching"
                    label="From the makers of spaCy"
                    to="https://prodi.gy"
                    button="Try it out"
                    background="#f6f6f6"
                    color="#000"
                    small
                >
                    <Link to="https://prodi.gy" hidden>
                        {/** Update image */}
                        <img
                            src={prodigyImage}
                            alt="Prodigy: Radically efficient machine teaching"
                        />
                    </Link>
                    <br />
                    <br />
                    Prodigy is an <strong>annotation tool</strong> so efficient that data scientists
                    can do the annotation themselves, enabling a new level of rapid iteration.
                    Whether you're working on entity recognition, intent detection or image
                    classification, Prodigy can help you <strong>train and evaluate</strong> your
                    models faster.
                </LandingBanner>
            </LandingBannerGrid>

            <LandingGrid cols={2} style={{ gridTemplateColumns: '1fr calc(80ch + 14rem)' }}>
                <LandingCol>
                    <H2>Reproducible training for custom pipelines</H2>
                    <p>
                        spaCy v3.0 introduces a comprehensive and extensible system for{' '}
                        <strong>configuring your training runs</strong>. Your configuration file
                        will describe every detail of your training run, with no hidden defaults,
                        making it easy to <strong>rerun your experiments</strong> and track changes.
                        You can use the quickstart widget or the{' '}
                        <Link to="/api/cli#init-config">
                            <InlineCode>init config</InlineCode>
                        </Link>{' '}
                        command to get started, or clone a project template for an end-to-end
                        workflow.
                    </p>
                    <p>
                        <Button to="/usage/training">Get started</Button>
                    </p>
                </LandingCol>
                <LandingCol>
                    <QuickstartTraining />
                </LandingCol>
            </LandingGrid>

            <LandingGrid cols={2}>
                <LandingCol>
                    <Link to="/usage/projects" hidden>
                        <img src={projectsImage} />
                    </Link>
                    <br />
                    <br />
                    <br />
                    <Project id="pipelines/tagger_parser_ud" title="Get started">
                        The easiest way to get started is to clone a project template and run it
                        – for example, this template for training a{' '}
                        <strong>part-of-speech tagger</strong> and{' '}
                        <strong>dependency parser</strong> on a Universal Dependencies treebank.
                    </Project>
                </LandingCol>
                <LandingCol>
                    <H2>End-to-end workflows from prototype to production</H2>
                    <p>
                        spaCy's new project system gives you a smooth path from prototype to
                        production. It lets you keep track of all those{' '}
                        <strong>data transformation</strong>, preprocessing and{' '}
                        <strong>training steps</strong>, so you can make sure your project is always
                        ready to hand over for automation. It features source asset download,
                        command execution, checksum verification, and caching with a variety of
                        backends and integrations.
                    </p>
                    <p>
                        <Button to="/usage/projects">Try it out</Button>
                    </p>
                </LandingCol>
            </LandingGrid>

            <LandingBannerGrid>
                <LandingBanner
                    to="https://course.spacy.io"
                    button="Start the course"
                    background="#f6f6f6"
                    color="#252a33"
                    small
                >
                    <Link to="https://course.spacy.io" hidden>
                        <img
                            src={courseImage}
                            alt="Advanced NLP with spaCy: A free online course"
                        />
                    </Link>
                    <br />
                    <br />
                    In this <strong>free and interactive online course</strong> you’ll learn how to
                    use spaCy to build advanced natural language understanding systems, using both
                    rule-based and machine learning approaches. It includes{' '}
                    <strong>55 exercises</strong> featuring videos, slide decks, multiple-choice
                    questions and interactive coding practice in the browser.
                </LandingBanner>
                <LandingBanner
                    title="spaCy IRL: Two days of NLP"
                    label="Watch the videos"
                    to="https://www.youtube.com/playlist?list=PLBmcuObd5An4UC6jvK_-eSl6jCvP1gwXc"
                    button="Watch the videos"
                    background="#ffc194"
                    backgroundImage={irlBackground}
                    color="#1a1e23"
                    small
                >
                    We were pleased to invite the spaCy community and other folks working on NLP to
                    Berlin for a small and intimate event. We booked a beautiful venue, hand-picked
                    an awesome lineup of speakers and scheduled plenty of social time to get to know
                    each other. The YouTube playlist includes 12 talks about NLP research,
                    development and applications, with keynotes by Sebastian Ruder (DeepMind) and
                    Yoav Goldberg (Allen AI).
                </LandingBanner>
            </LandingBannerGrid>

            <LandingGrid cols={2} style={{ gridTemplateColumns: '1fr 60%' }}>
                <LandingCol>
                    <H2>Benchmarks</H2>
                    <p>
                        spaCy v3.0 introduces transformer-based pipelines that bring spaCy's
                        accuracy right up to the current <strong>state-of-the-art</strong>. You can
                        also use a CPU-optimized pipeline, which is less accurate but much cheaper
                        to run.
                    </p>
                    <p>
                        <Button to="/usage/facts-figures#benchmarks">More results</Button>
                    </p>
                </LandingCol>

                <LandingCol>
                    <Benchmarks />
                </LandingCol>
            </LandingGrid>
        </>
    )
}

Landing.propTypes = {
    data: PropTypes.shape({
        repo: PropTypes.string,
        languages: PropTypes.arrayOf(
            PropTypes.shape({
                models: PropTypes.arrayOf(PropTypes.string),
            })
        ),
    }),
}

export default () => (
    <StaticQuery query={landingQuery} render={({ site }) => <Landing data={site.siteMetadata} />} />
)

const landingQuery = graphql`
    query LandingQuery {
        site {
            siteMetadata {
                nightly
                repo
                counts {
                    langs
                    modelLangs
                    starterLangs
                    models
                    starters
                }
            }
        }
    }
`

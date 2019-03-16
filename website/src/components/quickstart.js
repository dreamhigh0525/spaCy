import React, { Fragment, useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import { window } from 'browser-monads'

import Section from './section'
import Icon from './icon'
import { H2 } from './typography'
import classes from '../styles/quickstart.module.sass'

function getNewChecked(optionId, checkedForId, multiple) {
    if (!multiple) return [optionId]
    if (checkedForId.includes(optionId)) return checkedForId.filter(opt => opt !== optionId)
    return [...checkedForId, optionId]
}

const Quickstart = ({ data, title, description, id, children }) => {
    const [styles, setStyles] = useState({})
    const [checked, setChecked] = useState({})
    const [initialized, setInitialized] = useState(false)

    const getCss = (id, checkedOptions) => {
        const checkedForId = checkedOptions[id] || []
        const exclude = checkedForId
            .map(value => `:not([data-quickstart-${id}="${value}"])`)
            .join('')
        return `[data-quickstart-results]>[data-quickstart-${id}]${exclude} {display: none}`
    }

    useEffect(() => {
        window.dispatchEvent(new Event('resize')) // scroll position for progress
        if (!initialized) {
            const initialChecked = Object.assign(
                {},
                ...data.map(({ id, options }) => ({
                    [id]: options.filter(option => option.checked).map(({ id }) => id),
                }))
            )
            const initialStyles = Object.assign(
                {},
                ...data.map(({ id }) => ({ [id]: getCss(id, initialChecked) }))
            )
            setChecked(initialChecked)
            setStyles(initialStyles)
            setInitialized(true)
        }
    }, [data, initialized])

    return !data.length ? null : (
        <Section id={id}>
            <div className={classes.root}>
                {title && (
                    <H2 className={classes.title} name={id}>
                        <a href={`#${id}`}>{title}</a>
                    </H2>
                )}

                {description && <p className={classes.description}>{description}</p>}

                {data.map(({ id, title, options = [], multiple, help }) => (
                    <div key={id} data-quickstart-group={id} className={classes.group}>
                        <style data-quickstart-style={id}>
                            {styles[id] ||
                                `[data-quickstart-results]>[data-quickstart-${id}] { display: none }`}
                        </style>
                        <div className={classes.legend}>
                            {title}
                            {help && (
                                <span data-tooltip={help} className={classes.help}>
                                    {' '}
                                    <Icon name="help" width={16} spaced />
                                </span>
                            )}
                        </div>
                        <div className={classes.fields}>
                            {options.map(option => {
                                const optionType = multiple ? 'checkbox' : 'radio'
                                const checkedForId = checked[id] || []
                                return (
                                    <Fragment key={option.id}>
                                        <input
                                            onChange={() => {
                                                const newChecked = {
                                                    ...checked,
                                                    [id]: getNewChecked(
                                                        option.id,
                                                        checkedForId,
                                                        multiple
                                                    ),
                                                }
                                                setChecked(newChecked)
                                                setStyles({
                                                    ...styles,
                                                    [id]: getCss(id, newChecked),
                                                })
                                            }}
                                            type={optionType}
                                            className={classNames(
                                                classes.input,
                                                classes[optionType]
                                            )}
                                            name={id}
                                            id={`quickstart-${option.id}`}
                                            value={option.id}
                                            checked={checkedForId.includes(option.id)}
                                        />
                                        <label
                                            className={classes.label}
                                            htmlFor={`quickstart-${option.id}`}
                                        >
                                            {option.title}
                                            {option.meta && (
                                                <span className={classes.meta}>{option.meta}</span>
                                            )}
                                            {option.help && (
                                                <span
                                                    data-tooltip={option.help}
                                                    className={classes.help}
                                                >
                                                    {' '}
                                                    <Icon name="help" width={16} spaced />
                                                </span>
                                            )}
                                        </label>
                                    </Fragment>
                                )
                            })}
                        </div>
                    </div>
                ))}
                <pre className={classes.code}>
                    <code className={classes.results} data-quickstart-results="">
                        {children}
                    </code>
                </pre>
            </div>
        </Section>
    )
}

Quickstart.defaultProps = {
    data: [],
    id: 'quickstart',
}

Quickstart.propTypes = {
    title: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
    description: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
    data: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.string.isRequired,
            title: PropTypes.string.isRequired,
            multiple: PropTypes.bool,
            options: PropTypes.arrayOf(
                PropTypes.shape({
                    id: PropTypes.string.isRequired,
                    title: PropTypes.string.isRequired,
                    checked: PropTypes.bool,
                    help: PropTypes.string,
                })
            ),
            help: PropTypes.string,
        })
    ),
}

const QS = ({ children, prompt = 'bash', divider = false, ...props }) => {
    const qsClassNames = classNames({
        [classes.prompt]: !!prompt && !divider,
        [classes.bash]: prompt === 'bash' && !divider,
        [classes.python]: prompt === 'python' && !divider,
        [classes.divider]: !!divider,
    })
    const attrs = Object.assign(
        {},
        ...Object.keys(props).map(key => ({
            [`data-quickstart-${key}`]: props[key],
        }))
    )
    return (
        <span className={qsClassNames} {...attrs}>
            {children}
        </span>
    )
}

export { Quickstart, QS }

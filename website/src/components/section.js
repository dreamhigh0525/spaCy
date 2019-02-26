import React, { useEffect } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
import 'intersection-observer'
import { useInView } from 'react-intersection-observer'
import { window } from 'browser-monads'

import classes from '../styles/section.module.sass'

const Section = ({ id, className, ...props }) => {
    const sectionClassNames = classNames(classes.root, className)
    const relId = id && id.startsWith('section-') ? id.slice(8) : id
    const [ref, inView] = useInView({ threshold: 0 })

    useEffect(() => {
        if (inView && relId) {
            window.dispatchEvent(new CustomEvent('inview', { detail: relId }))
        }
    })
    return <section ref={ref} id={id} className={sectionClassNames} {...props} />
}

Section.propTypes = {
    id: PropTypes.string,
    className: PropTypes.string,
}

export default Section

export const Hr = () => <hr className={classes.hr} />

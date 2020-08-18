import React from 'react'
import classNames from 'classnames'

import Icon from './icon'
import { isString } from './util'
import classes from '../styles/table.module.sass'

function isNum(children) {
    return isString(children) && /^\d+[.,]?[\dx]+?(|x|ms|mb|gb|k|m)?$/i.test(children)
}

function getCellContent(children) {
    const icons = {
        '✅': { name: 'yes', variant: 'success' },
        '❌': { name: 'no', variant: 'error' },
    }

    if (isString(children) && icons[children.trim()]) {
        const iconProps = icons[children.trim()]
        return <Icon {...iconProps} />
    }
    // Work around prettier auto-escape
    if (isString(children) && children.startsWith('\\')) {
        return children.slice(1)
    }
    return children
}

function isDividerRow(children) {
    if (children.length && children[0].props && children[0].props.name == 'td') {
        const tdChildren = children[0].props.children
        if (tdChildren && !Array.isArray(tdChildren) && tdChildren.props) {
            return tdChildren.props.name === 'em'
        }
    }
    return false
}

function isFootRow(children) {
    const rowRegex = /^(RETURNS|YIELDS|CREATES|PRINTS|EXECUTES)/
    if (children.length && children[0].props.name === 'td') {
        const cellChildren = children[0].props.children
        if (
            cellChildren &&
            cellChildren.props &&
            cellChildren.props.children &&
            isString(cellChildren.props.children)
        ) {
            return rowRegex.test(cellChildren.props.children)
        }
    }
    return false
}

export const Table = ({ fixed, className, ...props }) => {
    const tableClassNames = classNames(classes.root, className, {
        [classes.fixed]: fixed,
    })
    return <table className={tableClassNames} {...props} />
}

export const Th = props => <th className={classes.th} {...props} />

export const Tr = ({ evenodd = true, children, ...props }) => {
    const foot = isFootRow(children)
    const isDivider = isDividerRow(children)
    const trClasssNames = classNames({
        [classes.tr]: evenodd,
        [classes.footer]: foot,
        [classes.divider]: isDivider,
        'table-footer': foot,
    })

    return (
        <tr className={trClasssNames} {...props}>
            {children}
        </tr>
    )
}

export const Td = ({ num, nowrap, className, children, ...props }) => {
    const content = getCellContent(children)
    const tdClassNames = classNames(classes.td, className, {
        [classes.num]: num || isNum(children),
        [classes.nowrap]: nowrap,
    })
    return (
        <td className={tdClassNames} {...props}>
            {content}
        </td>
    )
}

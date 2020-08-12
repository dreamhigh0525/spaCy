import React, { useState } from 'react'
import { StaticQuery, graphql } from 'gatsby'
import highlightCode from 'gatsby-remark-prismjs/highlight-code.js'

import { Quickstart, QS } from '../components/quickstart'
import generator from './quickstart-training-generator'
import { isString, htmlToReact } from '../components/util'

const DEFAULT_LANG = 'en'
const DEFAULT_HARDWARE = 'gpu'
const DEFAULT_OPT = 'efficiency'
const COMPONENTS = ['tagger', 'parser', 'ner', 'textcat']

const DATA = [
    {
        id: 'lang',
        title: 'Language',
        defaultValue: DEFAULT_LANG,
    },
    {
        id: 'components',
        title: 'Components',
        help: 'Pipeline components to train. Requires training data for those annotations.',
        options: COMPONENTS.map(id => ({ id, title: id })),
        multiple: true,
    },
    {
        id: 'hardware',
        title: 'Hardware',
        options: [
            { id: 'cpu', title: 'CPU preferred', checked: DEFAULT_HARDWARE === 'cpu' },
            { id: 'gpu', title: 'GPU', checked: DEFAULT_HARDWARE === 'gpu' },
        ],
    },
    {
        id: 'optimize',
        title: 'Optimize for',
        help: '...',
        options: [
            { id: 'efficiency', title: 'efficiency', checked: DEFAULT_OPT === 'efficiency' },
            { id: 'accuracy', title: 'accuracy', checked: DEFAULT_OPT === 'accuracy' },
        ],
    },
]

function stringify(value) {
    if (isString(value) && value.startsWith('${')) return value
    const string = JSON.stringify(value)
    if (Array.isArray(value)) return string.replace(/,/g, ', ')
    return string
}

export default function QuickstartTraining({ id, title, download = 'config.cfg' }) {
    const [lang, setLang] = useState(DEFAULT_LANG)
    const [components, setComponents] = useState([])
    const [[hardware], setHardware] = useState([DEFAULT_HARDWARE])
    const [[optimize], setOptimize] = useState([DEFAULT_OPT])
    const setters = {
        lang: setLang,
        components: setComponents,
        hardware: setHardware,
        optimize: setOptimize,
    }
    const content = generator({
        lang,
        pipeline: stringify(components),
        components,
        optimize,
        hardware,
    })
    const rawContent = content.trim().replace(/\n\n\n+/g, '\n\n')
    const displayContent = highlightCode('ini', rawContent)
        .split('\n')
        .map(line => (line.startsWith('#') ? `<span class="token comment">${line}</span>` : line))
        .join('\n')
    return (
        <StaticQuery
            query={query}
            render={({ site }) => {
                const langs = site.siteMetadata.languages
                DATA[0].dropdown = langs.map(({ name, code }) => ({
                    id: code,
                    title: name,
                }))
                return (
                    <Quickstart
                        download={download}
                        rawContent={content}
                        data={DATA}
                        title={title}
                        id={id}
                        setters={setters}
                        hidePrompts
                        small
                        codeLang="ini"
                    >
                        {htmlToReact(displayContent)}
                    </Quickstart>
                )
            }}
        />
    )
}

const query = graphql`
    query QuickstartTrainingQuery {
        site {
            siteMetadata {
                languages {
                    code
                    name
                }
            }
        }
    }
`

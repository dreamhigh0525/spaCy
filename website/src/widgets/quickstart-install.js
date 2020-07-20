import React from 'react'
import { StaticQuery, graphql } from 'gatsby'

import { Quickstart, QS } from '../components/quickstart'
import { repo } from '../components/util'

const DATA = [
    {
        id: 'os',
        title: 'Operating system',
        options: [
            { id: 'mac', title: 'macOS / OSX', checked: true },
            { id: 'windows', title: 'Windows' },
            { id: 'linux', title: 'Linux' },
        ],
    },
    {
        id: 'package',
        title: 'Package manager',
        options: [
            { id: 'pip', title: 'pip', checked: true },
            { id: 'conda', title: 'conda' },
            { id: 'source', title: 'from source' },
        ],
    },
    {
        id: 'config',
        title: 'Configuration',
        multiple: true,
        options: [
            {
                id: 'venv',
                title: 'virtualenv',
                help: 'Use a virtual environment and install spaCy into a user directory',
            },
        ],
    },
    {
        id: 'data',
        title: 'Additional data',
        multiple: true,
        options: [
            {
                id: 'lookups',
                title: 'Lemmatization',
                help: 'Install additional lookup tables and rules for lemmatization',
            },
        ],
    },
]

const QuickstartInstall = ({ id, title }) => (
    <StaticQuery
        query={query}
        render={({ site }) => {
            const models = site.siteMetadata.languages.filter(({ models }) => models !== null)
            const data = [
                ...DATA,
                {
                    id: 'models',
                    title: 'Models',
                    multiple: true,
                    options: models.map(({ code, name }) => ({ id: code, title: name })),
                },
            ]
            return (
                <Quickstart data={data} title={title} id={id}>
                    <QS config="venv">python -m venv .env</QS>
                    <QS config="venv" os="mac">
                        source .env/bin/activate
                    </QS>
                    <QS config="venv" os="linux">
                        source .env/bin/activate
                    </QS>
                    <QS config="venv" os="windows">
                        .env\Scripts\activate
                    </QS>
                    <QS package="pip">pip install -U spacy</QS>
                    <QS package="conda">conda install -c conda-forge spacy</QS>
                    <QS package="source">git clone https://github.com/{repo}</QS>
                    <QS package="source">cd spaCy</QS>
                    <QS package="source" os="linux">
                        export PYTHONPATH=`pwd`
                    </QS>
                    <QS package="source" os="windows">
                        set PYTHONPATH=C:\path\to\spaCy
                    </QS>
                    <QS package="source">pip install -r requirements.txt</QS>
                    <QS data="lookups" package="pip">
                        pip install -U spacy-lookups-data
                    </QS>
                    <QS data="lookups" package="source">
                        pip install -U spacy-lookups-data
                    </QS>
                    <QS data="lookups" package="conda">
                        conda install -c conda-forge spacy-lookups-data
                    </QS>
                    <QS package="source">python setup.py build_ext --inplace</QS>
                    {models.map(({ code, models: modelOptions }) => (
                        <QS models={code} key={code}>
                            python -m spacy download {modelOptions[0]}
                        </QS>
                    ))}
                </Quickstart>
            )
        }}
    />
)

export default QuickstartInstall

const query = graphql`
    query QuickstartInstallQuery {
        site {
            siteMetadata {
                languages {
                    code
                    name
                    models
                }
            }
        }
    }
`

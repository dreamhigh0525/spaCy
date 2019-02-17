import React, { useState, useEffect } from 'react'
import { window } from 'browser-monads'

import Link from '../components/link'
import { InlineCode } from '../components/code'
import { Label, H3 } from '../components/typography'
import { Table, Tr, Th, Td } from '../components/table'
import Infobox from '../components/infobox'
import { repo } from '../components/util'

function formatReleases(json) {
    return Object.values(json)
        .filter(release => release.name)
        .map(release => ({
            title:
                release.name.split(': ').length === 2 ? release.name.split(': ')[1] : release.name,
            url: release.html_url,
            date: release.published_at.split('T')[0],
            tag: release.tag_name,
            pre: release.prerelease,
        }))
}

const ChangelogTable = ({ data = [] }) => {
    return (
        <Table>
            <thead>
                <Tr>
                    <Th>Date</Th>
                    <Th>Version</Th>
                    <Th>Title</Th>
                </Tr>
            </thead>
            <tbody>
                {data.map(({ title, url, date, tag }) => (
                    <Tr key={tag}>
                        <Td nowrap>
                            <Label>{date}</Label>
                        </Td>
                        <Td>
                            <Link to={url} hideIcon>
                                <InlineCode>{tag}</InlineCode>
                            </Link>
                        </Td>
                        <Td>{title}</Td>
                    </Tr>
                ))}
            </tbody>
        </Table>
    )
}

const Changelog = () => {
    const [initialized, setInitialized] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [isError, setIsError] = useState(true)
    const [releases, setReleases] = useState([])
    const [prereleases, setPrereleases] = useState([])

    useEffect(() => {
        window.dispatchEvent(new Event('resize')) // scroll position for progress
        if (!initialized && repo) {
            setIsError(false)
            setIsLoading(true)
            fetch(`https://api.github.com/repos/${repo}/releases`)
                .then(res => res.json())
                .then(json => {
                    const releases = formatReleases(json)
                    setReleases(releases.filter(release => !release.pre))
                    setPrereleases(releases.filter(release => release.pre))
                    setIsLoading(false)
                })
                .catch(err => {
                    setIsLoading(false)
                    setIsError(true)
                })
            setInitialized(true)
        }
    }, [])

    const error = (
        <Infobox title="Unable to load changelog from GitHub" variant="danger">
            <p>
                Please see the
                <Link to={`https://github.com/${repo}/releases`} ws hideIcon>
                    releases page
                </Link>
                instead.
            </p>
        </Infobox>
    )

    return isError ? (
        error
    ) : isLoading ? null : (
        <>
            <H3>Stable Releases</H3>
            <ChangelogTable data={releases} />

            <H3>Pre-Releases</H3>

            <p>
                Pre-releases include alpha and beta versions, as well as release candidates. They
                are not intended for production use. You can download spaCy pre-releases via the{' '}
                <InlineCode>spacy-nightly</InlineCode> package on pip.
            </p>

            <ChangelogTable data={prereleases} />
        </>
    )
}

export default Changelog

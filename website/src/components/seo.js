import React from 'react'
import PropTypes from 'prop-types'
import Helmet from 'react-helmet'
import { StaticQuery, graphql } from 'gatsby'

import socialImageDefault from '../images/social_default.jpg'
import socialImageApi from '../images/social_api.jpg'
import socialImageUniverse from '../images/social_universe.jpg'

function getPageTitle(title, sitename, slogan, sectionTitle) {
    if (sectionTitle) {
        return `${title} · ${sitename} ${sectionTitle}`
    }
    if (title) {
        return `${title} · ${sitename}`
    }
    return `${sitename} · ${slogan}`
}

function getImage(section) {
    if (section === 'api') return socialImageApi
    if (section === 'universe') return socialImageUniverse
    return socialImageDefault
}

const SEO = ({ description, lang, title, section, sectionTitle, bodyClass }) => (
    <StaticQuery
        query={query}
        render={data => {
            const siteMetadata = data.site.siteMetadata
            const metaDescription = description || siteMetadata.description
            const pageTitle = getPageTitle(
                title,
                siteMetadata.title,
                siteMetadata.slogan,
                sectionTitle
            )
            const socialImage = getImage(section)
            const meta = [
                {
                    name: 'description',
                    content: metaDescription,
                },
                {
                    property: 'og:title',
                    content: pageTitle,
                },
                {
                    property: 'og:description',
                    content: metaDescription,
                },
                {
                    property: 'og:type',
                    content: `website`,
                },
                {
                    property: 'og:site_name',
                    content: title,
                },
                {
                    property: 'og:image',
                    content: socialImage,
                },
                {
                    name: 'twitter:card',
                    content: 'summary_large_image',
                },
                {
                    name: 'twitter:image',
                    content: socialImage,
                },
                {
                    name: 'twitter:creator',
                    content: `@${data.site.siteMetadata.social.twitter}`,
                },
                {
                    name: 'twitter:site',
                    content: `@${data.site.siteMetadata.social.twitter}`,
                },
                {
                    name: 'twitter:title',
                    content: pageTitle,
                },
                {
                    name: 'twitter:description',
                    content: metaDescription,
                },
                {
                    name: 'docsearch:language',
                    content: lang,
                },
            ]

            return (
                <Helmet
                    htmlAttributes={{ lang }}
                    bodyAttributes={{ class: bodyClass }}
                    title={pageTitle}
                    meta={meta}
                />
            )
        }}
    />
)

SEO.defaultProps = {
    lang: 'en',
}

SEO.propTypes = {
    description: PropTypes.string,
    lang: PropTypes.string,
    meta: PropTypes.array,
    keywords: PropTypes.arrayOf(PropTypes.string),
    title: PropTypes.string,
    section: PropTypes.string,
    bodyClass: PropTypes.string,
}

export default SEO

const query = graphql`
    query DefaultSEOQuery {
        site {
            siteMetadata {
                title
                description
                slogan
                siteUrl
                email
                social {
                    twitter
                }
            }
        }
    }
`

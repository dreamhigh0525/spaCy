const autoprefixer = require('autoprefixer')
const path = require('path')

// https://florian.ec/blog/gatsby-build-netlify-segmentation-fault/
const sharp = require('sharp')
sharp.cache(false)
sharp.simd(false)

// Markdown plugins
const wrapSectionPlugin = require('./src/plugins/remark-wrap-section.js')
const customAttrsPlugin = require('./src/plugins/remark-custom-attrs.js')
const codeBlocksPlugin = require('./src/plugins/remark-code-blocks.js')

// Import metadata
const site = require('./meta/site.json')
const sidebars = require('./meta/sidebars.json')
const models = require('./meta/languages.json')
const universe = require('./meta/universe.json')

const DEFAULT_TEMPLATE = path.resolve('./src/templates/index.js')

const isNightly = !!+process.env.SPACY_NIGHTLY || site.nightlyBranches.includes(process.env.BRANCH)
const favicon = isNightly ? `src/images/icon_nightly.png` : `src/images/icon.png`
const binderBranch = isNightly ? 'nightly' : site.binderBranch
const siteUrl = isNightly ? site.siteUrlNightly : site.siteUrl
const domain = isNightly ? site.domainNightly : site.domain
const branch = isNightly ? 'develop' : 'master'

// Those variables are going to be replaced in the Markdown, e.g. %%GITHUB_SPACY
const replacements = {
    GITHUB_SPACY: `https://github.com/explosion/spaCy/tree/${branch}`,
    GITHUB_PROJECTS: `https://github.com/${site.projectsRepo}`,
}

/**
 * Compute the overall total counts of models and languages
 */
function getCounts(langs = []) {
    return {
        langs: langs.length,
        modelLangs: langs.filter(({ models }) => models && !!models.length).length,
        starterLangs: langs.filter(({ starters }) => starters && !!starters.length).length,
        models: langs.map(({ models }) => (models ? models.length : 0)).reduce((a, b) => a + b, 0),
        starters: langs
            .map(({ starters }) => (starters ? starters.length : 0))
            .reduce((a, b) => a + b, 0),
    }
}

module.exports = {
    siteMetadata: {
        ...site,
        sidebars,
        ...models,
        counts: getCounts(models.languages),
        universe,
        nightly: isNightly,
        binderBranch,
        siteUrl,
    },

    plugins: [
        {
            resolve: `gatsby-plugin-svgr`,
            options: {
                svgo: false,
                svgoConfig: {
                    removeViewBox: false,
                },
            },
        },
        {
            resolve: `gatsby-plugin-sass`,
            options: {
                indentedSyntax: true,
                postCssPlugins: [autoprefixer()],
                cssLoaderOptions: {
                    localIdentName:
                        process.env.NODE_ENV == 'development'
                            ? '[name]-[local]-[hash:8]'
                            : '[hash:8]',
                },
            },
        },
        `gatsby-plugin-react-helmet`,
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                name: `docs`,
                path: `${__dirname}/docs`,
            },
        },
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                name: `pages`,
                path: `${__dirname}/src/pages`,
            },
        },
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                name: `images`,
                path: `${__dirname}/src/images`,
            },
        },
        {
            resolve: `gatsby-source-filesystem`,
            options: {
                name: `docsImages`,
                path: `${__dirname}/docs/images`,
            },
        },
        {
            resolve: `gatsby-mdx`,
            options: {
                root: __dirname,
                extensions: ['.md', '.mdx'],
                defaultLayouts: {
                    pages: DEFAULT_TEMPLATE,
                },
                mdPlugins: [customAttrsPlugin, wrapSectionPlugin, codeBlocksPlugin],
                gatsbyRemarkPlugins: [
                    {
                        resolve: `gatsby-remark-smartypants`,
                        options: {
                            backticks: false,
                            dashes: 'oldschool',
                        },
                    },
                    {
                        resolve: `gatsby-remark-images`,
                        options: {
                            maxWidth: 650,
                            linkImagesToOriginal: true,
                            sizeByPixelDensity: false,
                            showCaptions: true,
                            quality: 80,
                            withWebp: { quality: 80 },
                            wrapperStyle: { marginBottom: '20px' },
                        },
                    },
                    {
                        // NB: This need to run after gatsby-remark-images!
                        resolve: `gatsby-remark-unwrap-images`,
                    },
                    {
                        resolve: `gatsby-remark-copy-linked-files`,
                    },
                    {
                        resolve: 'gatsby-remark-find-replace',
                        options: {
                            replacements,
                            prefix: '%%',
                        },
                    },
                ],
            },
        },
        `gatsby-transformer-sharp`,
        `gatsby-plugin-sharp`,
        `gatsby-plugin-catch-links`,
        `gatsby-plugin-sitemap`,
        {
            resolve: `gatsby-plugin-manifest`,
            options: {
                name: site.title,
                short_name: site.title,
                start_url: `/`,
                background_color: site.theme,
                theme_color: site.theme,
                display: `minimal-ui`,
                icon: favicon,
            },
        },
        {
            resolve: `gatsby-plugin-plausible`,
            options: { domain },
        },
        {
            resolve: 'gatsby-plugin-robots-txt',
            options: {
                host: siteUrl,
                sitemap: `${siteUrl}/sitemap.xml`,
                // If we're in a special state (nightly, legacy) prevent indexing
                resolveEnv: () => (isNightly ? 'development' : 'production'),
                env: {
                    production: {
                        policy: [{ userAgent: '*', allow: '/' }],
                    },
                    development: {
                        policy: [{ userAgent: '*', disallow: ['/'] }],
                    },
                },
            },
        },
        `gatsby-plugin-offline`,
    ],
}

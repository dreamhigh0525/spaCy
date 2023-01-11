# spacy.io website and docs

![Netlify Status](https://api.netlify.com/api/v1/badges/d65fe97d-99ab-47f8-a339-1d8987251da0/deploy-status)

The styleguide for the spaCy website is available at
[spacy.io/styleguide](https://spacy.io/styleguide).

## Setup and installation

```bash
# Clone the repository
git clone https://github.com/explosion/spaCy
cd spaCy/website

# Switch to the correct Node version
#
# If you don't have NVM and don't want to use it, you can manually switch to the Node version
# stated in /.nvmrc and skip this step
nvm use

# Install the dependencies
npm install

# Start the development server
npm run dev
```

If you are planning on making edits to the site, you should also set up the
[Prettier](https://prettier.io/) code formatter. It takes care of formatting
Markdown and other files automatically.
[See here](https://prettier.io/docs/en/editors.html) for the available
extensions for your code editor. The
[`.prettierrc`](https://github.com/explosion/spaCy/tree/master/website/.prettierrc)
file in the root defines the settings used in this codebase.

## Building & developing the site with Docker

While it shouldn't be necessary and is not recommended you can run this site in a Docker container.

If you'd like to do this, **be sure you do _not_ include your local
`node_modules` folder**, since there are some dependencies that need to be built
for the image system. Rename it before using.

```bash
docker run -it \
  -v $(pwd):/spacy-io/website \
  -p 8000:8000 \
  ghcr.io/explosion/spacy-io \
  gatsby develop -H 0.0.0.0
```

This will allow you to access the built website at http://0.0.0.0:8000/ in your
browser, and still edit code in your editor while having the site reflect those
changes.

**Note**: If you're working on a Mac with an M1 processor, you might see
segfault errors from `qemu` if you use the default image. To fix this use the
`arm64` tagged image in the `docker run` command
(ghcr.io/explosion/spacy-io:arm64).

### Building the Docker image

If you'd like to build the image locally, you can do so like this:

```bash
docker build -t spacy-io .
```

This will take some time, so if you want to use the prebuilt image you'll save a
bit of time.

## Project structure

```yaml
├── docs                 # the actual markdown content
├── meta                 # JSON-formatted site metadata
|   ├── dynamicMeta.js   # At build time generated meta data
|   ├── languages.json   # supported languages and statistical models
|   ├── sidebars.json    # sidebar navigations for different sections
|   ├── site.json        # general site metadata
|   ├── type-annotations.json # Type annotations
|   └── universe.json    # data for the spaCy universe section
├── pages                # Next router pages
├── public               # static images and other assets
├── setup                # Jinja setup
├── src                  # source
|   ├── components       # React components
|   ├── fonts            # webfonts
|   ├── images           # images used in the layout
|   ├── plugins          # custom plugins to transform Markdown
|   ├── styles           # CSS modules and global styles
|   ├── templates        # page layouts
|   |   ├── docs.js      # layout template for documentation pages
|   |   ├── index.js     # global layout template
|   |   ├── models.js    # layout template for model pages
|   |   └── universe.js  # layout templates for universe
|   └── widgets          # non-reusable components with content, e.g. changelog
├── .eslintrc.json       # ESLint config file
├── .nvmrc               # NVM config file
|                        # (to support "nvm use" to switch to correct Node version)
|
├── .prettierrc          # Prettier config file
├── next.config.mjs      # Next config file
├── package.json         # package settings and dependencies
└── tsconfig.json        # TypeScript config file
```

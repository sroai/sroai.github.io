import { defineConfig } from "vitepress";
import lightbox from "vitepress-plugin-lightbox"


export default defineConfig({
    title: 'SRO AI',
    description: 'AI for Streaming Readout: real-time signal and background separation in nuclear physics data streams',
    base: '/',

    // The repository README describes the repo, not a site page
    srcExclude: ['README.md', '**/README.md', '.claude/**'],

    head: [
        ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ],

    themeConfig: {
        nav: [
            { text: 'Home', link: '/' },
            { text: 'Data', link: '/ai-epic-background/data' },
            {
                text: 'Projects',
                items: [
                    { text: 'EIC AI Background', link: '/ai-epic-background/' },
                    { text: 'eic2ai converter', link: 'https://github.com/sroai/eic2ai' },
                    { text: 'Meson Structure', link: 'https://jeffersonlab.github.io/meson-structure/' },
                ]
            },
            { text: 'GitHub', link: 'https://github.com/sroai' },
        ],

        // The landing page has no sidebar; each project section has its own
        sidebar: {
            '/ai-epic-background/': [
                {
                    text: 'Getting Started',
                    collapsed: false,
                    items: [
                        { text: 'Overview', link: '/ai-epic-background/' },
                        { text: 'Data Format', link: '/ai-epic-background/data-format' },
                    ]
                },
                {
                    text: 'Data',
                    collapsed: false,
                    items: [
                        { text: 'Available Datasets', link: '/ai-epic-background/data' },
                    ]
                },
                {
                    text: 'Campaigns',
                    collapsed: false,
                    items: [
                        { text: '26.04.1-stable', link: '/ai-epic-background/campaign_2026-04/' },
                    ]
                },
                {
                    text: 'CSV Convert',
                    collapsed: false,
                    items: [
                        { text: 'Overview', link: '/ai-epic-background/csv-convert' },
                        { text: 'Running the Converter', link: '/ai-epic-background/csv-convert-running' },
                        { text: 'Batch on SLURM', link: '/ai-epic-background/csv-convert-snakemake' },
                    ]
                },
                {
                    text: 'Full-Sim Pipeline',
                    collapsed: false,
                    items: [
                        { text: 'Overview', link: '/ai-epic-background/full-sim-pipeline' },
                        { text: 'Job Creator', link: '/ai-epic-background/full-sim-pipeline-jobs' },
                        { text: 'Campaigns', link: '/ai-epic-background/full-sim-pipeline-campaigns' },
                        { text: 'Backgrounds', link: '/ai-epic-background/background' },
                    ]
                },
                {
                    text: 'AI / ML',
                    collapsed: false,
                    items: [
                        { text: 'Datasets', link: '/ai-epic-background/ai-datasets' },
                    ]
                },
            ],
        },

        footer: {
            message: 'Released under the MIT License.',
            copyright: 'Copyright © 2026 SRO AI'
        },

        socialLinks: [
            { icon: 'github', link: 'https://github.com/sroai' }
        ],

        search: {
            provider: 'local'
        },

        outline: {
            level: [2, 3],
            label: 'On this page'
        },

        editLink: {
            pattern: 'https://github.com/sroai/sroai.github.io/edit/main/:path',
            text: 'Edit this page on GitHub'
        },

        appearance: true
    },

    markdown: {
        config: (md) => {
            md.use(lightbox, {});
        }
    },

    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    additionalData: `
            // Add any global SCSS variables here
          `
                }
            }
        }
    }
});

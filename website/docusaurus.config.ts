import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Hyper Stack Manager',
  tagline: 'Environment Hypervisor for Modern Hybrid Stacks',
  favicon: 'img/logo-v2.svg',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  // future: {
  //   v4: true, // Improve compatibility with the upcoming Docusaurus v4
  // },

  // Set the production url of your site here
  url: 'https://VLMHyperBenchTeam.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/hsm/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'VLMHyperBenchTeam', // Usually your GitHub org/user name.
  projectName: 'hsm', // Usually your repo name.

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'ru',
    locales: ['ru'],
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  themes: ['@docusaurus/theme-mermaid'],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/VLMHyperBenchTeam/hsm/tree/main/hsm/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    mermaid: {
      theme: {
        light: 'dark',
        dark: 'dark',
      },
    },
    // Replace with your project's social card
    image: 'img/social-card.png',
    navbar: {
      title: 'HSM',
      logo: {
        alt: 'HSM Logo',
        src: 'img/logo-v2.svg',
        srcDark: 'img/logo-v2.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Документация',
        },
        {
          href: 'https://github.com/VLMHyperBenchTeam/hsm',
          label: 'GitHub',
          position: 'left',
        },
        {
          href: 'https://github.com/VLMHyperBenchTeam/hsm/issues',
          label: 'Обратная связь',
          position: 'left',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [],
      copyright: `Copyright © ${new Date().getFullYear()} HyperTeam. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

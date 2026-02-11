import React from 'react';
import DocItemLayout from '@theme-original/DocItem/Layout';
import type DocItemLayoutType from '@theme/DocItem/Layout';
import type {WrapperProps} from '@docusaurus/types';
import DocsColorModeToggle from '@site/src/components/DocsColorModeToggle';

type Props = WrapperProps<typeof DocItemLayoutType>;

export default function DocItemLayoutWrapper(props: Props): React.JSX.Element {
  return (
    <>
      <DocItemLayout {...props} />
    </>
  );
}
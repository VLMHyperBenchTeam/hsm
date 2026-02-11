import React from 'react';
import NavbarLayout from '@theme-original/Navbar/Layout';
import type NavbarLayoutType from '@theme/Navbar/Layout';
import type {WrapperProps} from '@docusaurus/types';
import DocsColorModeToggle from '@site/src/components/DocsColorModeToggle';
import useIsBrowser from '@docusaurus/useIsBrowser';

type Props = WrapperProps<typeof NavbarLayoutType>;

export default function NavbarLayoutWrapper(props: Props): React.JSX.Element {
  const isBrowser = useIsBrowser();
  const isHomePage = isBrowser && (window.location.pathname === '/hsm/' || window.location.pathname === '/hsm');

  return (
    <div className="relative">
      <NavbarLayout {...props} />
      {!isHomePage && (
        <div
          className="navbar__item"
          style={{
            position: 'absolute',
            right: '1rem',
            top: '50%',
            transform: 'translateY(-50%)',
            zIndex: 1000,
          }}
        >
          <DocsColorModeToggle />
        </div>
      )}
    </div>
  );
}
import React, {useCallback} from 'react';
import useIsBrowser from '@docusaurus/useIsBrowser';
import {useColorMode} from '@docusaurus/theme-common';
import styles from './styles.module.css';

export default function DocsColorModeToggle() {
  const isBrowser = useIsBrowser();
  const {colorMode, setColorMode} = useColorMode();

  const toggle = useCallback(() => {
    setColorMode(colorMode === 'dark' ? 'light' : 'dark');
  }, [colorMode, setColorMode]);

  // Avoid hydration mismatch
  if (!isBrowser) {
    return null;
  }

  return (
    <button
      aria-label="Toggle color mode"
      onClick={toggle}
      className={styles.toggleButton}
    >
      {colorMode === 'dark' ? (
        <span className="flex items-center gap-2">
          <span className="material-symbols-outlined text-sm">light_mode</span>
          <span className="font-mono text-xs uppercase tracking-widest">Light Mode</span>
        </span>
      ) : (
        <span className="flex items-center gap-2">
          <span className="material-symbols-outlined text-sm">dark_mode</span>
          <span className="font-mono text-xs uppercase tracking-widest">Dark Mode</span>
        </span>
      )}
    </button>
  );
}
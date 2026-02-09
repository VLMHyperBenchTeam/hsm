import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import NeuralBackground from '@site/src/components/NeuralBackground';

export default function Home(): React.JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  
  return (
    <Layout
      title={siteConfig.title}
      description={siteConfig.tagline}
      noFooter={true}>
      <NeuralBackground />
      
      <div className="relative z-40 w-full min-h-screen flex flex-col items-center justify-center p-4 md:p-12 pt-24">
        
        {/* Main Title Section */}
        <div className="text-center mb-16 relative">
          <h1 className="font-display text-5xl md:text-7xl font-bold text-white tracking-tight mb-4 neon-text-cyan">
            HYPER STACK <span className="text-secondary neon-text-lime">MANAGER</span>
          </h1>
          <p className="font-mono text-slate-300 text-sm md:text-base tracking-widest uppercase opacity-80">
            Environment Hypervisor for Modern Hybrid Stacks
          </p>
          
          {/* Quick Start Button */}
          <div className="mt-12 flex justify-center">
            <Link
              to="/docs/intro"
              className="group relative inline-flex items-center justify-center px-8 py-4 font-display font-bold border transition-all duration-300 no-underline backdrop-blur-sm quick-start-button-fixed"
              style={{
                clipPath: 'polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px)'
              }}
            >
              <span className="mr-3 text-lg font-mono">{'>'}_</span>
              <span className="tracking-[0.2em]">QUICK START - 5 MIN</span>
              
              {/* Decorative corner arrow */}
              <svg className="absolute -bottom-1 -right-1 w-4 h-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform group-hover:translate-x-1 group-hover:translate-y-1"
                   style={{ color: '#00FFCC' }}
                   viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M7 17L17 17L17 7" />
              </svg>
            </Link>
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-7xl px-4">
          
          {/* Card 1: Lego Architecture */}
          <div className="group relative bg-[#0e1116]/10 backdrop-blur-sm border border-primary/10 p-8 hover:border-primary/40 transition-all duration-500 hover:bg-[#0e1116]/30 hover:shadow-[0_0_30px_rgba(0,255,204,0.05)]"
               style={{
                 clipPath: 'polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px)'
               }}>
            {/* Top decorative line */}
            <div className="absolute top-0 left-0 w-20 h-[1px] bg-primary/30"></div>
            <div className="absolute top-0 left-0 w-[1px] h-4 bg-primary/30"></div>
            
            {/* Top right dots */}
            <div className="absolute top-3 right-3 flex gap-1 opacity-40">
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
            </div>
            
            <div className="mb-6 text-primary">
              <span className="material-symbols-outlined text-5xl drop-shadow-[0_0_10px_rgba(0,255,204,0.5)]">deployed_code</span>
            </div>
            
            <h3 className="font-display text-xl font-bold text-secondary mb-4 uppercase tracking-wide">
              Lego-Architecture
            </h3>
            
            <p className="font-mono text-sm text-slate-400 leading-relaxed">
              Assemble your stack from independent components. Easily swap out implementation interfaces (e.g., one vector DB for another) with a single command.
            </p>
          </div>

          {/* Card 2: Hybrid Orchestration */}
          <div className="group relative bg-[#0e1116]/10 backdrop-blur-sm border border-primary/10 p-8 hover:border-primary/40 transition-all duration-500 hover:bg-[#0e1116]/30 hover:shadow-[0_0_30px_rgba(0,255,204,0.05)]"
               style={{
                 clipPath: 'polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px)'
               }}>
            {/* Top decorative line */}
            <div className="absolute top-0 left-0 w-20 h-[1px] bg-primary/30"></div>
            <div className="absolute top-0 left-0 w-[1px] h-4 bg-primary/30"></div>

            {/* Top right dots */}
            <div className="absolute top-3 right-3 flex gap-1 opacity-40">
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
            </div>

            <div className="mb-6 text-primary">
              <span className="material-symbols-outlined text-5xl drop-shadow-[0_0_10px_rgba(0,255,204,0.5)]">dns</span>
            </div>
            
            <h3 className="font-display text-xl font-bold text-secondary mb-4 uppercase tracking-wide">
              Hybrid Orchestration
            </h3>
            
            <p className="font-mono text-sm text-slate-400 leading-relaxed">
              Unified management of Python packages (via uv) and infrastructure services (via docker compose) in a single manifest.
            </p>
          </div>

          {/* Card 3: Atomic Synchronization */}
          <div className="group relative bg-[#0e1116]/10 backdrop-blur-sm border border-primary/10 p-8 hover:border-primary/40 transition-all duration-500 hover:bg-[#0e1116]/30 hover:shadow-[0_0_30px_rgba(0,255,204,0.05)]"
               style={{
                 clipPath: 'polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px)'
               }}>
            {/* Top decorative line */}
            <div className="absolute top-0 left-0 w-20 h-[1px] bg-primary/30"></div>
            <div className="absolute top-0 left-0 w-[1px] h-4 bg-primary/30"></div>

            {/* Top right dots */}
            <div className="absolute top-3 right-3 flex gap-1 opacity-40">
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
              <div className="w-1 h-1 bg-primary rounded-full"></div>
            </div>

            <div className="mb-6 text-primary">
              <span className="material-symbols-outlined text-5xl drop-shadow-[0_0_10px_rgba(0,255,204,0.5)]">sync_lock</span>
            </div>
            
            <h3 className="font-display text-xl font-bold text-secondary mb-4 uppercase tracking-wide">
              Atomic Synchronization
            </h3>
            
            <p className="font-mono text-sm text-slate-400 leading-relaxed">
              Transactional configuration updates. If dependencies don't resolve, your working files remain in a stable state.
            </p>
          </div>

        </div>

        {/* Footer Status Bar */}
        <div className="fixed bottom-0 left-0 right-0 h-8 bg-[#0e1116] border-t border-[#1e1e1e] flex items-center justify-between px-6 z-50">
          <div className="flex items-center gap-6 text-[10px] font-mono text-slate-500">
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
              <span className="text-primary/80">DOCS: SYNCHRONIZED | v0.0.1</span>
            </div>
          </div>
          
          <div className="flex items-center gap-4 text-[10px] font-mono text-slate-500">
            <span className="hidden md:inline">Copyright © 2026 HyperTeam</span>
            <span className="text-secondary">SYSTEM_STATUS: READY</span>
          </div>
        </div>

      </div>
    </Layout>
  );
}

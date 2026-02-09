import React from 'react';

const NeuralBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,#0f1319_0%,#05070a_100%)]"></div>
      <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter height="200%" id="glow" width="200%" x="-50%" y="-50%">
            <feGaussianBlur result="coloredBlur" stdDeviation="2.5"></feGaussianBlur>
            <feMerge>
              <feMergeNode in="coloredBlur"></feMergeNode>
              <feMergeNode in="SourceGraphic"></feMergeNode>
            </feMerge>
          </filter>
        </defs>
        <g className="animate-float-slow opacity-20" stroke="#DAFF00" strokeWidth="0.5">
          <line x1="10%" x2="25%" y1="10%" y2="25%"></line>
          <line x1="25%" x2="15%" y1="25%" y2="45%"></line>
          <line x1="15%" x2="40%" y1="45%" y2="35%"></line>
          <line x1="40%" x2="60%" y1="35%" y2="15%"></line>
          <line x1="60%" x2="80%" y1="15%" y2="25%"></line>
          <line x1="80%" x2="70%" y1="25%" y2="55%"></line>
          <line x1="70%" x2="90%" y1="55%" y2="75%"></line>
          <line x1="25%" x2="50%" y1="25%" y2="50%"></line>
          <line x1="50%" x2="70%" y1="50%" y2="55%"></line>
          <line x1="10%" x2="30%" y1="80%" y2="70%"></line>
          <line x1="30%" x2="50%" y1="70%" y2="90%"></line>
          <line x1="50%" x2="70%" y1="90%" y2="80%"></line>
        </g>
        <g className="animate-float-slow opacity-40" fill="#00FFCC" filter="url(#glow)">
          <circle cx="10%" cy="10%" r="2"></circle>
          <circle cx="25%" cy="25%" r="3"></circle>
          <circle cx="15%" cy="45%" r="2"></circle>
          <circle cx="40%" cy="35%" r="2"></circle>
          <circle cx="60%" cy="15%" r="3"></circle>
          <circle cx="80%" cy="25%" r="2"></circle>
          <circle cx="70%" cy="55%" r="3"></circle>
          <circle cx="90%" cy="75%" r="2"></circle>
          <circle cx="50%" cy="50%" r="2"></circle>
          <circle cx="10%" cy="80%" r="2"></circle>
          <circle cx="30%" cy="70%" r="3"></circle>
          <circle cx="50%" cy="90%" r="2"></circle>
          <circle cx="70%" cy="80%" r="2"></circle>
        </g>
        <g className="animate-float-delayed" opacity="0.6" stroke="#DAFF00" strokeWidth="1">
          <line className="animate-pulse-glow" x1="5%" x2="20%" y1="40%" y2="60%"></line>
          <line className="animate-pulse-glow" style={{animationDelay: '1s'}} x1="20%" x2="45%" y1="60%" y2="55%"></line>
          <line className="animate-pulse-glow" style={{animationDelay: '2s'}} x1="45%" x2="65%" y1="55%" y2="75%"></line>
          <line className="animate-pulse-glow" style={{animationDelay: '0.5s'}} x1="65%" x2="95%" y1="75%" y2="60%"></line>
          <line className="animate-pulse-glow" style={{animationDelay: '1.5s'}} x1="35%" x2="45%" y1="15%" y2="55%"></line>
          <line className="animate-pulse-glow" style={{animationDelay: '2.5s'}} x1="65%" x2="75%" y1="75%" y2="95%"></line>
        </g>
        <g className="animate-float-delayed" fill="#00FFCC" filter="url(#glow)">
          <circle className="animate-node-pulse" cx="5%" cy="40%" r="3"></circle>
          <circle className="animate-node-pulse" cx="20%" cy="60%" r="4" style={{animationDelay: '1s'}}></circle>
          <circle className="animate-node-pulse" cx="45%" cy="55%" r="3" style={{animationDelay: '2s'}}></circle>
          <circle className="animate-node-pulse" cx="65%" cy="75%" r="5" style={{animationDelay: '0.5s'}}></circle>
          <circle className="animate-node-pulse" cx="95%" cy="60%" r="3" style={{animationDelay: '1.5s'}}></circle>
          <circle className="animate-node-pulse" cx="35%" cy="15%" r="3" style={{animationDelay: '0.8s'}}></circle>
          <circle className="animate-node-pulse" cx="75%" cy="95%" r="2" style={{animationDelay: '2.2s'}}></circle>
        </g>
      </svg>
      <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,204,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,204,0.03)_1px,transparent_1px)] bg-[size:40px_40px] opacity-20 pointer-events-none"></div>
    </div>
  );
};

export default NeuralBackground;
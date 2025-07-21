import React from 'react';
import ReactDOM from 'react-dom/client';
// Imports
import { Tldraw } from 'tldraw'
import 'tldraw/tldraw.css'
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div style={{ position: 'fixed', inset: 0 }}>
      <Tldraw inferDarkMode persistenceKey="tldraw" />
    </div>
  </React.StrictMode>
);

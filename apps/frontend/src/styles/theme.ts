import type React from 'react';

export const createGlobalStyles = (): React.CSSProperties => ({
  margin: 0,
  padding: 0,
  boxSizing: 'border-box',
});

export const colors = {
  primary: '#FF7A3D',
  primaryDark: '#E85A1A',
  success: '#6ECFB0',
  error: '#E86B6B',
  warning: '#F0C96A',
  background: '#FFFAF6',
  secondaryBg: '#FFF3EB',
  text: '#2D1F14',
  textSecondary: '#9C7B66',
  border: '#F5DDD0',
  divider: '#FAE8DC',
  shadow: 'rgba(200, 100, 50, 0.10)',

  // Bento pastel palette (warm orange/peach tones)
  pastelPink:    '#FFE8E0',
  pastelMint:    '#FFF0E6',
  pastelLavender:'#FFE9D9',
  pastelPeach:   '#FFEADE',
  pastelBlue:    '#FFE4D4',
  pastelYellow:  '#FFF4E0',
  pastelCoral:   '#FFD9C8',
  pastelSage:    '#FAEEE4',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
};

export const typography = {
  title: {
    fontSize: '24px',
    fontWeight: 600,
    lineHeight: '1.4',
  },
  heading: {
    fontSize: '18px',
    fontWeight: 600,
    lineHeight: '1.3',
  },
  subtitle: {
    fontSize: '16px',
    fontWeight: 500,
    lineHeight: '1.3',
  },
  body: {
    fontSize: '15px',
    fontWeight: 400,
    lineHeight: '1.4',
  },
  bodySmall: {
    fontSize: '14px',
    fontWeight: 400,
    lineHeight: '1.4',
  },
  caption: {
    fontSize: '12px',
    fontWeight: 400,
    lineHeight: '1.3',
    color: '#65676b',
  },
};

export const borderRadius = {
  xs: '6px',
  sm: '12px',
  md: '16px',
  lg: '22px',
  xl: '28px',
};

export const globalStyles = `
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  html, body, #root {
    width: 100%;
    height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  body {
    background-color: #FFFAF6;
    color: #2D1F14;
  }

  button {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
    cursor: pointer;
    border: none;
    outline: none;
  }

  input, textarea, select {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
  }

  input:focus, textarea:focus, select:focus {
    outline: none;
  }

  ::placeholder {
    color: #99a2ad;
  }

  ::-webkit-scrollbar {
    width: 6px;
  }

  ::-webkit-scrollbar-track {
    background: transparent;
  }

  ::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #999;
  }
`;

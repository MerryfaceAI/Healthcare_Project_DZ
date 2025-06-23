// src/styled.d.ts
import 'styled-components';
declare module 'styled-components' {
  export interface DefaultTheme {
    sidebarBg:    string;
    sidebarHover: string;
    topbarBg:     string;
    appBg:        string;
    cardBg?:      string;
    btnPrimary?:  string;
    text?:        string;
  }
}

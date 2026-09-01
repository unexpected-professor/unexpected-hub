// Primary navigation. Organised by subject matter, not by internal course
// identifiers such as CM1 / TD2 (hub section 5.1). Legal and privacy pages are
// added to the footer in a later commit.
export interface NavItem {
  label: string;
  href: string;
}

export const primaryNav: NavItem[] = [
  { label: 'Accueil', href: '/' },
  { label: 'À propos', href: '/about' },
  { label: 'Leçons', href: '/lessons' },
  { label: 'Laboratoires', href: '/labs' },
];

export const footerNav: NavItem[] = [
  { label: 'Licence et attribution', href: '/licence' },
  { label: 'Confidentialité', href: '/confidentialite' },
  { label: 'Mentions légales', href: '/mentions-legales' },
  { label: 'Contact', href: '/contact' },
];

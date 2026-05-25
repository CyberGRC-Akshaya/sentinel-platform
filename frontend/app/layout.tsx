import "./globals.css";

export const metadata = {
  title: "Sentinel Assurance Platform",
  description: "AI-native assurance intelligence by Eye On Bits"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

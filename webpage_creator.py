#!/usr/bin/env python3
"""Generate a simple static website from the command line."""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


def parse_feature_items(raw_features: Sequence[str] | None) -> List[Tuple[str, str]]:
    """Convert a sequence like ['Fast:Responsive', 'Secure:Reliable'] to pairs."""
    if not raw_features:
        return [
            ("Fast", "Built for speed and clean user experiences."),
            ("Responsive", "Looks great on desktop, tablet, and mobile."),
            ("Simple", "Easy to customize for your own brand."),
        ]

    features: List[Tuple[str, str]] = []
    for entry in raw_features:
        if ":" in entry:
            title, description = entry.split(":", 1)
            features.append((title.strip(), description.strip()))
        else:
            features.append((entry.strip(), "A useful section for your website."))
    return features


def parse_list_items(raw_items: Sequence[str] | None, default_items: Iterable[str]) -> List[str]:
    """Parse simple name:value entries or fallback defaults."""
    if not raw_items:
        return list(default_items)
    return [item.strip() for item in raw_items if item.strip()]


def build_styles(theme_color: str = "#2563eb", dark_mode: bool = False) -> str:
    background = "#020817" if dark_mode else "#f8fafc"
    panel = "#0f172a" if dark_mode else "#ffffff"
    panel_alt = "#111827" if dark_mode else "#f8fafc"
    text = "#e2e8f0" if dark_mode else "#0f172a"
    muted = "#cbd5e1" if dark_mode else "#475569"
    border = "rgba(148, 163, 184, 0.18)" if dark_mode else "rgba(148, 163, 184, 0.25)"
    gradient = "linear-gradient(180deg, #0b1120 0%, #020817 30%, #020817 100%)" if dark_mode else "linear-gradient(180deg, #eff6ff 0%, #f8fafc 20%, #f8fafc 100%)"
    card_shadow = "rgba(15, 23, 42, 0.5)" if dark_mode else "rgba(15, 23, 42, 0.08)"
    return f"""
:root {{
    --accent: {theme_color};
    --accent-dark: #1d4ed8;
    --bg: {background};
    --bg-soft: {panel_alt};
    --card: {panel};
    --card-soft: rgba(15, 23, 42, 0.7);
    --text: {text};
    --muted: {muted};
    --shadow: {card_shadow};
    --border: {border};
    --button-light: #ffffff;
    --button-dark: #0f172a;
}}

* {{
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    color: var(--text);
    background: {gradient};
    line-height: 1.6;
}}

img {{
    max-width: 100%;
    display: block;
}}

.container {{
    width: min(1100px, calc(100% - 2rem));
    margin: 0 auto;
}}

header {{
    background: rgba(15, 23, 42, 0.72);
    backdrop-filter: blur(14px);
    position: sticky;
    top: 0;
    z-index: 10;
    border-bottom: 1px solid var(--border);
}}

nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 72px;
    gap: 1rem;
}}

.brand {{
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 1.5rem;
    padding: 0;
    margin: 0;
    color: var(--muted);
    font-size: 0.95rem;
}}

.nav-links a {{
    color: inherit;
    text-decoration: none;
}}

.hero {{
    padding: 4.5rem 0 3rem;
}}

.hero-grid {{
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    align-items: center;
    gap: 2rem;
}}

.eyebrow {{
    display: inline-block;
    background: rgba(37, 99, 235, 0.12);
    color: #60a5fa;
    border-radius: 999px;
    padding: 0.45rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}}

h1 {{
    font-size: clamp(2.5rem, 5vw, 4.3rem);
    line-height: 1.1;
    margin: 1rem 0 1rem;
}}

.lead {{
    max-width: 38rem;
    font-size: 1.1rem;
    color: var(--muted);
    margin-bottom: 1.5rem;
}}

.cta-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 1.5rem;
}}

.button {{
    display: inline-block;
    padding: 0.9rem 1.5rem;
    border-radius: 0.8rem;
    text-decoration: none;
    font-weight: 700;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.button:hover {{
    transform: translateY(-1px);
}}

.button.primary {{
    background: var(--accent);
    color: white;
    box-shadow: 0 12px 24px rgba(37, 99, 235, 0.2);
}}

.button.secondary {{
    background: var(--button-light);
    color: var(--button-dark);
    border: 1px solid var(--border);
}}

.hero-card, .feature-card, .testimonial-card, .pricing-card, .contact-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 1.25rem;
    box-shadow: 0 18px 40px var(--shadow);
}}

.hero-card {{
    padding: 1.5rem;
}}

.mockup {{
    background: var(--bg-soft);
    border-radius: 1rem;
    border: 1px solid var(--border);
    padding: 1rem;
}}

.stat-row {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin-top: 1rem;
}}

.stat-box {{
    padding: 0.8rem;
    border-radius: 0.75rem;
    background: var(--card);
    border: 1px solid var(--border);
}}

.stat-box strong {{
    display: block;
    font-size: 1.25rem;
    color: var(--accent-dark);
}}

main {{
    padding-bottom: 4rem;
}}

.section {{
    padding-top: 2rem;
}}

.section-title {{
    text-align: center;
    margin-bottom: 2rem;
}}

.section-title h2 {{
    font-size: clamp(1.9rem, 3vw, 2.7rem);
    margin: 0.5rem 0 0;
}}

.feature-grid, .testimonial-grid, .pricing-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem;
}}

.feature-card, .testimonial-card, .pricing-card {{
    padding: 1.5rem;
}}

.feature-icon {{
    width: 2.8rem;
    height: 2.8rem;
    display: grid;
    place-items: center;
    border-radius: 0.8rem;
    background: rgba(37, 99, 235, 0.12);
    color: #60a5fa;
    font-size: 1.3rem;
    margin-bottom: 0.9rem;
}}

.feature-card h3, .pricing-card h3, .testimonial-card h3 {{
    margin: 0 0 0.5rem;
    font-size: 1.2rem;
}}

.feature-card p, .testimonial-card p, .pricing-card p {{
    margin: 0;
    color: var(--muted);
}}

.meta-row {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin: 0.75rem 0 1rem;
}}

.price {{
    font-size: 2rem;
    font-weight: 700;
}}

.price span {{
    font-size: 0.9rem;
    color: var(--muted);
}}

ul.meta-list {{
    list-style: none;
    margin: 1rem 0 0;
    padding: 0;
    display: grid;
    gap: 0.5rem;
    color: var(--muted);
}}

ul.meta-list li::before {{
    content: "✓ ";
    color: var(--accent);
    font-weight: 700;
}}

.testimonial-card strong {{
    display: block;
    margin-top: 1rem;
    font-size: 0.95rem;
}}

.contact-card {{
    padding: 2rem;
    margin-top: 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
    color: white;
}}

.contact-card .button.secondary {{
    background: white;
    color: var(--accent-dark);
    border: none;
}}

form.contact-form {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
}}

input, textarea {{
    width: 100%;
    padding: 0.9rem 1rem;
    border-radius: 0.75rem;
    border: 1px solid var(--border);
    background: rgba(255, 255, 255, 0.08);
    color: var(--text);
}}

input::placeholder, textarea::placeholder {{
    color: var(--muted);
}}

textarea {{
    min-height: 120px;
    resize: vertical;
}}

footer {{
    padding: 2rem 0 3rem;
    color: var(--muted);
    text-align: center;
}}

@media (max-width: 760px) {{
    nav {{
        flex-direction: column;
        justify-content: center;
        padding: 1rem 0;
    }}

    .hero-grid {{
        grid-template-columns: 1fr;
    }}

    .nav-links {{
        gap: 0.8rem;
        flex-wrap: wrap;
        justify-content: center;
    }}

    .stat-row {{
        grid-template-columns: 1fr;
    }}
}}
"""


def escape_html(value: str) -> str:
    return html.escape(value, quote=True)


def build_page(
    title: str,
    subtitle: str,
    description: str,
    button_text: str,
    features: Sequence[Tuple[str, str]],
    theme_color: str,
    dark_mode: bool = False,
    contact_email: str = "hello@example.com",
    testimonials: Sequence[Tuple[str, str]] | None = None,
    pricing: Sequence[Tuple[str, str, List[str]]] | None = None,
) -> str:
    safe_title = escape_html(title)
    safe_subtitle = escape_html(subtitle)
    safe_description = escape_html(description)
    safe_button_text = escape_html(button_text)
    safe_email = escape_html(contact_email)

    nav_links = [
        ("Home", "#top"),
        ("Features", "#features"),
        ("Testimonials", "#testimonials"),
        ("Pricing", "#pricing"),
        ("Contact", "#contact"),
    ]

    feature_cards = "\n".join(
        f"""
        <article class=\"feature-card\">
            <div class=\"feature-icon\">{index + 1}</div>
            <h3>{escape_html(feature_title)}</h3>
            <p>{escape_html(feature_description)}</p>
        </article>
        """.strip()
        for index, (feature_title, feature_description) in enumerate(features)
    )

    default_testimonials = [
        ("Alicia M.", "The page feels premium, clear, and ready to convert visitors into customers."),
        ("James T.", "We launched our service faster than expected and our leads went up immediately."),
        ("Rina S.", "It looks polished, loads quickly, and helps our brand stand out online."),
    ]
    testimonial_cards = "\n".join(
        f"""
        <article class=\"testimonial-card\">
            <p>“{escape_html(quote)}”</p>
            <strong>{escape_html(name)}</strong>
        </article>
        """.strip()
        for name, quote in (testimonials or default_testimonials)
    )

    default_pricing = [
        ("Starter", "$29", ["One landing page", "Custom branding", "Email support"]),
        ("Growth", "$79", ["Everything in Starter", "More sections", "Priority support"]),
        ("Scale", "$149", ["Everything in Growth", "A/B testing layout", "Dedicated onboarding"]),
    ]
    pricing_cards = "\n".join(
        f"""
        <article class=\"pricing-card\">
            <h3>{escape_html(title_value)}</h3>
            <div class=\"meta-row\">
                <div class=\"price\">{escape_html(price)}<span>/mo</span></div>
            </div>
            <ul class=\"meta-list\">
                {''.join(f'<li>{escape_html(item)}</li>' for item in items)}
            </ul>
        </article>
        """.strip()
        for title_value, price, items in (pricing or default_pricing)
    )

    body_class = "theme-dark" if dark_mode else "theme-light"

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{safe_title}</title>
    <meta name=\"description\" content=\"{safe_description}\" />
    <link rel=\"stylesheet\" href=\"styles.css\" />
</head>
<body id=\"top\" class=\"{body_class}\">
    <header>
        <div class=\"container\">
            <nav>
                <div class=\"brand\">{safe_title}</div>
                <ul class=\"nav-links\">
                    {''.join(f'<li><a href="{href}">{label}</a></li>' for label, href in nav_links)}
                </ul>
            </nav>
        </div>
    </header>

    <section class=\"hero\">
        <div class=\"container hero-grid\">
            <div>
                <span class=\"eyebrow\">Launch faster</span>
                <h1>{safe_title}</h1>
                <p class=\"lead\">{safe_subtitle}</p>
                <p class=\"lead\">{safe_description}</p>
                <div class=\"cta-row\">
                    <a class=\"button primary\" href=\"#contact\">{safe_button_text}</a>
                    <a class=\"button secondary\" href=\"#features\">View features</a>
                </div>
            </div>

            <div class=\"hero-card\">
                <div class=\"mockup\">
                    <div style=\"display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;\">
                        <strong>Overview</strong>
                        <span style=\"background: rgba(37, 99, 235, 0.08); color: var(--accent-dark); padding: .35rem .6rem; border-radius: 999px; font-size: .75rem; font-weight: 700;\">Live</span>
                    </div>
                    <div style=\"height: 12px; width: 70%; background: rgba(37, 99, 235, 0.15); border-radius: 999px; margin-bottom: 1rem;\"></div>
                    <div style=\"height: 12px; width: 90%; background: rgba(148, 163, 184, 0.2); border-radius: 999px; margin-bottom: 1rem;\"></div>
                    <div style=\"height: 12px; width: 60%; background: rgba(148, 163, 184, 0.2); border-radius: 999px; margin-bottom: 1.2rem;\"></div>
                    <div class=\"stat-row\">
                        <div class=\"stat-box\"><strong>24/7</strong> Support</div>
                        <div class=\"stat-box\"><strong>10x</strong> Faster</div>
                        <div class=\"stat-box\"><strong>99%</strong> Uptime</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <main>
        <section id=\"features\" class=\"section\">
            <div class=\"container\">
                <div class=\"section-title\">
                    <span class=\"eyebrow\">Features</span>
                    <h2>Everything you need for a polished launch</h2>
                </div>
                <div class=\"feature-grid\">
                    {feature_cards}
                </div>
            </div>
        </section>

        <section id=\"testimonials\" class=\"section\">
            <div class=\"container\">
                <div class=\"section-title\">
                    <span class=\"eyebrow\">Testimonials</span>
                    <h2>People love how it feels</h2>
                </div>
                <div class=\"testimonial-grid\">
                    {testimonial_cards}
                </div>
            </div>
        </section>

        <section id=\"pricing\" class=\"section\">
            <div class=\"container\">
                <div class=\"section-title\">
                    <span class=\"eyebrow\">Pricing</span>
                    <h2>Simple plans for every stage</h2>
                </div>
                <div class=\"pricing-grid\">
                    {pricing_cards}
                </div>
            </div>
        </section>

        <section id=\"contact\" class=\"section\">
            <div class=\"container\">
                <div class=\"contact-card\">
                    <div>
                        <strong style=\"display:block; font-size:1.6rem; margin-bottom:0.4rem;\">Ready to build something bigger?</strong>
                        <span>Use this modern starter and customize it for your brand, product, or portfolio.</span>
                    </div>
                    <div>
                        <form class=\"contact-form\" action=\"mailto:{safe_email}\" method=\"post\" enctype=\"text/plain\">
                            <input type=\"text\" placeholder=\"Your name\" aria-label=\"Your name\" />
                            <input type=\"email\" placeholder=\"Your email\" aria-label=\"Your email\" />
                            <textarea placeholder=\"Tell us about your project\" aria-label=\"Project details\"></textarea>
                            <button class=\"button secondary\" type=\"submit\">Send message</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <div class=\"container\">
            © 2026 {safe_title}. All rights reserved.
        </div>
    </footer>
</body>
</html>
"""


def create_project(
    output_dir: Path,
    title: str,
    subtitle: str,
    description: str,
    button_text: str,
    theme_color: str,
    features: Sequence[Tuple[str, str]],
    dark_mode: bool = False,
    contact_email: str = "hello@example.com",
    testimonials: Sequence[Tuple[str, str]] | None = None,
    pricing: Sequence[Tuple[str, str, List[str]]] | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    index_html = build_page(
        title,
        subtitle,
        description,
        button_text,
        features,
        theme_color,
        dark_mode,
        contact_email,
        testimonials,
        pricing,
    )
    css = build_styles(theme_color, dark_mode)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    (output_dir / "styles.css").write_text(css, encoding="utf-8")
    return output_dir / "index.html"


def interactive_prompt() -> argparse.Namespace:
    title = input("Website title: ") or "My New Website"
    subtitle = input("Short headline: ") or "Build a modern online presence with a polished landing page."
    description = input("Description: ") or "This starter page is designed to showcase your product, service, or portfolio in a clean and professional way."
    button_text = input("Call to action text: ") or "Get Started"
    theme_color = input("Theme color (hex): ") or "#2563eb"
    dark_mode = input("Use dark mode? (y/N): ").strip().lower() in {"y", "yes", "true", "1"}
    feature_input = input("Features (format: Name:Description, Name:Description): ") or ""
    raw_features = [item.strip() for item in feature_input.split(",") if item.strip()] if feature_input else None
    return argparse.Namespace(
        title=title,
        subtitle=subtitle,
        description=description,
        button_text=button_text,
        theme_color=theme_color,
        dark_mode=dark_mode,
        output_dir=Path("website"),
        features=raw_features,
        contact_email="hello@example.com",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a modern static website from the command line.")
    parser.add_argument("--title", default="My New Website", help="Web page title")
    parser.add_argument("--subtitle", default="Build a modern online presence with a polished landing page.", help="Main headline text")
    parser.add_argument("--description", default="This starter page is designed to showcase your product, service, or portfolio in a clean and professional way.", help="Short description below the headline")
    parser.add_argument("--button-text", default="Get Started", help="Text shown in the main call-to-action button")
    parser.add_argument("--theme-color", default="#2563eb", help="Accent color for the page in hex format")
    parser.add_argument("--dark-mode", action="store_true", help="Enable dark mode styling")
    parser.add_argument("--output-dir", default="website", help="Directory to store the generated files")
    parser.add_argument("--feature", dest="features", action="append", default=[], help="Feature in the format Name:Description. Can be used multiple times.")
    parser.add_argument("--contact-email", default="hello@example.com", help="Email used by the contact form")
    args = parser.parse_args()

    if not any([
        args.title != "My New Website",
        args.subtitle != "Build a modern online presence with a polished landing page.",
        args.description != "This starter page is designed to showcase your product, service, or portfolio in a clean and professional way.",
        args.button_text != "Get Started",
        args.theme_color != "#2563eb",
        args.dark_mode,
        args.features,
        args.contact_email != "hello@example.com",
    ]):
        if sys.stdin.isatty():
            prompt_args = interactive_prompt()
            args.title = prompt_args.title
            args.subtitle = prompt_args.subtitle
            args.description = prompt_args.description
            args.button_text = prompt_args.button_text
            args.theme_color = prompt_args.theme_color
            args.dark_mode = prompt_args.dark_mode
            args.output_dir = str(prompt_args.output_dir)
            args.features = prompt_args.features
            args.contact_email = prompt_args.contact_email

    features = parse_feature_items(args.features)
    output_path = create_project(
        Path(args.output_dir),
        args.title,
        args.subtitle,
        args.description,
        args.button_text,
        args.theme_color,
        features,
        dark_mode=args.dark_mode,
        contact_email=args.contact_email,
    )
    print(f"Website generated successfully: {output_path.parent}")
    print(f"Open {output_path} in your browser to view it.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled. No files were created.")

import { useMemo, useState } from "react";

type Page =
  | "home" | "categories" | "products" | "detail" | "search" | "wishlist"
  | "cart" | "checkout" | "confirmation" | "orders" | "order-detail"
  | "tracking" | "profile" | "notifications" | "support" | "login";
type IconName = "search" | "heart" | "cart" | "bell" | "user" | "menu" | "chevron"
  | "star" | "arrow" | "truck" | "shield" | "refresh" | "grid" | "list"
  | "filter" | "x" | "check" | "package" | "home" | "card" | "help" | "logout";

const PHOTOS = {
  hero: "https://images.unsplash.com/photo-1715559522419-db7face19c1c?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=85&w=1400",
  fashion: "https://images.unsplash.com/photo-1668615522855-020131790355?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=80&w=900",
  beauty: "https://images.unsplash.com/photo-1784256543053-076f2a8e4e40?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=80&w=900",
  beauty2: "https://images.unsplash.com/photo-1783905326791-c1fb6b8bc113?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=80&w=900",
  lifestyle: "https://images.unsplash.com/photo-1696394375423-4a43cae6f6f4?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=80&w=900",
  fashion2: "https://images.unsplash.com/photo-1643075621108-00ddbe129d52?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&q=80&w=900",
};

const products = [
  { id: 1, name: "Everyday Structured Tote", brand: "Atelier No. 8", price: 128, was: 160, rating: 4.8, reviews: 248, image: PHOTOS.fashion, badge: "20% OFF", stock: "In stock", category: "Fashion" },
  { id: 2, name: "Radiance Skin Ritual Set", brand: "Aster & Moss", price: 74, was: 98, rating: 4.7, reviews: 189, image: PHOTOS.beauty, badge: "24% OFF", stock: "In stock", category: "Beauty" },
  { id: 3, name: "Daily Essential Sunglasses", brand: "North Standard", price: 92, was: 115, rating: 4.6, reviews: 96, image: PHOTOS.beauty2, badge: "20% OFF", stock: "Only 4 left", category: "Accessories" },
  { id: 4, name: "Relaxed Linen Co-ord", brand: "Morrow", price: 119, was: 149, rating: 4.9, reviews: 312, image: PHOTOS.lifestyle, badge: "BESTSELLER", stock: "In stock", category: "Fashion" },
  { id: 5, name: "Cloud Cotton Lounge Set", brand: "Soft Form", price: 86, was: 110, rating: 4.5, reviews: 143, image: PHOTOS.fashion2, badge: "NEW", stock: "In stock", category: "Home & Living" },
  { id: 6, name: "Renewal Night Serum", brand: "Aster & Moss", price: 58, was: 72, rating: 4.8, reviews: 207, image: PHOTOS.beauty2, badge: "19% OFF", stock: "Out of stock", category: "Beauty" },
];

const categories = [
  ["Fashion", "New season essentials", PHOTOS.fashion],
  ["Beauty", "Care, simplified", PHOTOS.beauty],
  ["Home & Living", "Considered comfort", PHOTOS.fashion2],
  ["Accessories", "The finishing touch", PHOTOS.beauty2],
  ["Electronics", "Smarter everyday", PHOTOS.lifestyle],
  ["Sports", "Move with purpose", PHOTOS.hero],
  ["Grocery", "Pantry favorites", PHOTOS.beauty],
  ["Books", "Stories worth keeping", PHOTOS.fashion2],
];

function Icon({ name, size = 20 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, React.ReactNode> = {
    search: <><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></>,
    heart: <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>,
    cart: <><path d="M3 3h2l2.4 11h9.8l2-7H6"/><circle cx="9" cy="19" r="1"/><circle cx="17" cy="19" r="1"/></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></>,
    user: <><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></>,
    menu: <><path d="M4 7h16M4 12h16M4 17h16"/></>,
    chevron: <path d="m9 18 6-6-6-6"/>,
    star: <path d="m12 2 3 6 7 .9-5 4.8 1.2 6.8L12 17.3l-6.2 3.2L7 13.7 2 8.9 9 8Z"/>,
    arrow: <><path d="M5 12h14"/><path d="m14 7 5 5-5 5"/></>,
    truck: <><path d="M3 6h11v11H3zM14 10h4l3 3v4h-7z"/><circle cx="7" cy="19" r="2"/><circle cx="18" cy="19" r="2"/></>,
    shield: <><path d="M12 3 4 6v5c0 5 3.5 8 8 10 4.5-2 8-5 8-10V6z"/><path d="m9 12 2 2 4-4"/></>,
    refresh: <><path d="M20 6v5h-5"/><path d="M18.5 16A8 8 0 1 1 20 11"/></>,
    grid: <><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></>,
    list: <><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></>,
    filter: <path d="M3 5h18l-7 8v6l-4 2v-8z"/>,
    x: <path d="m6 6 12 12M18 6 6 18"/>,
    check: <path d="m5 12 4 4L19 6"/>,
    package: <><path d="m12 3 9 5-9 5-9-5z"/><path d="m3 8 9 5 9-5v9l-9 5-9-5z"/></>,
    home: <><path d="m3 11 9-8 9 8"/><path d="M5 10v11h14V10M9 21v-7h6v7"/></>,
    card: <><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/></>,
    help: <><circle cx="12" cy="12" r="9"/><path d="M9.8 9a2.4 2.4 0 1 1 3.5 2.2c-.9.5-1.3 1-1.3 2M12 17h.01"/></>,
    logout: <><path d="M10 4H4v16h6M14 8l4 4-4 4M8 12h10"/></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden>{paths[name]}</svg>;
}

function Button({ children, onClick, variant = "primary", disabled = false, className = "" }: {
  children: React.ReactNode; onClick?: () => void; variant?: "primary" | "secondary" | "ghost"; disabled?: boolean; className?: string;
}) {
  return <button className={`btn btn-${variant} ${className}`} onClick={onClick} disabled={disabled}>{children}</button>;
}

function Header({ go, cartCount, mode, setMode }: { go: (p: Page) => void; cartCount: number; mode: "minimal" | "promo"; setMode: (m: "minimal" | "promo") => void }) {
  const [menu, setMenu] = useState(false);
  const [search, setSearch] = useState("");
  return <>
    <div className="announce">{mode === "promo" ? "FLASH EVENT — UP TO 40% OFF SELECTED EDITS" : "Complimentary delivery on orders over $75"} <span>Explore now</span></div>
    <header className="header">
      <button className="mobile-menu icon-btn" onClick={() => setMenu(!menu)}><Icon name="menu"/></button>
      <button className="logo" onClick={() => go("home")}>MONO<span>MARKET</span></button>
      <nav className={menu ? "nav open" : "nav"}>
        <button onClick={() => go("home")}>Home</button>
        <button onClick={() => go("categories")}>Categories</button>
        <button onClick={() => go("products")}>Shop</button>
        <button onClick={() => { go("products"); setMode("promo"); }}>Deals</button>
      </nav>
      <div className="header-search">
        <Icon name="search" size={18}/>
        <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && go("search")} placeholder="Search products, brands..." />
        {search && <button onClick={() => setSearch("")}><Icon name="x" size={16}/></button>}
      </div>
      <div className="header-actions">
        <button className="icon-btn hide-sm" onClick={() => go("wishlist")} aria-label="Wishlist"><Icon name="heart"/></button>
        <button className="icon-btn" onClick={() => go("cart")} aria-label="Cart"><Icon name="cart"/>{cartCount > 0 && <b>{cartCount}</b>}</button>
        <button className="icon-btn hide-sm" onClick={() => go("notifications")} aria-label="Notifications"><Icon name="bell"/><i/></button>
        <button className="profile-btn" onClick={() => go("profile")}><span>AS</span><small>Alex</small></button>
      </div>
    </header>
    <div className="stakeholder-bar">
      <span>Stakeholder preview</span>
      <div><button className={mode === "minimal" ? "active" : ""} onClick={() => setMode("minimal")}>UI Option A — Minimal</button><button className={mode === "promo" ? "active" : ""} onClick={() => setMode("promo")}>UI Option B — Promotional</button></div>
      <small>{mode === "minimal" ? "Calm, editorial & product-led" : "Offer-rich, energetic & discovery-led"}</small>
    </div>
  </>;
}

function Breadcrumb({ items, go }: { items: string[]; go: (p: Page) => void }) {
  return <div className="breadcrumb"><button onClick={() => go("home")}>Home</button>{items.map((x) => <span key={x}><Icon name="chevron" size={12}/>{x}</span>)}</div>;
}

function ProductCard({ product, go, add, wish, wished, compact = false }: {
  product: typeof products[0]; go: (p: Page) => void; add: (id: number) => void; wish: (id: number) => void; wished: boolean; compact?: boolean;
}) {
  return <article className={`product-card ${compact ? "compact" : ""}`}>
    <div className="product-image" onClick={() => go("detail")}>
      <img src={product.image} alt={product.name}/>
      <span className="badge">{product.badge}</span>
      <button className={`wish ${wished ? "active" : ""}`} onClick={(e) => { e.stopPropagation(); wish(product.id); }} aria-label="Toggle wishlist"><Icon name="heart" size={18}/></button>
      {product.stock === "Out of stock" && <div className="soldout">OUT OF STOCK</div>}
    </div>
    <div className="product-info">
      <div className="brand">{product.brand}</div>
      <button className="product-name" onClick={() => go("detail")}>{product.name}</button>
      <div className="rating"><Icon name="star" size={13}/><b>{product.rating}</b><span>({product.reviews})</span></div>
      <div className="price"><strong>${product.price}</strong><del>${product.was}</del><span>Save ${product.was - product.price}</span></div>
      <div className={`stock ${product.stock === "Out of stock" ? "out" : ""}`}>{product.stock}</div>
      <div className="card-actions">
        <Button onClick={() => add(product.id)} disabled={product.stock === "Out of stock"}>{product.stock === "Out of stock" ? "Unavailable" : "Add to cart"}</Button>
        <Button variant="secondary" onClick={() => go("detail")}>View</Button>
      </div>
    </div>
  </article>;
}

function Section({ title, eyebrow, children, action }: { title: string; eyebrow?: string; children: React.ReactNode; action?: () => void }) {
  return <section className="section">
    <div className="section-head"><div>{eyebrow && <span>{eyebrow}</span>}<h2>{title}</h2></div>{action && <button onClick={action}>View all <Icon name="arrow" size={16}/></button>}</div>
    {children}
  </section>;
}

function HomePage({ go, mode, add, wish, wishlist }: any) {
  return <>
    <main>
      <section className={`hero hero-${mode}`}>
        <div className="hero-copy">
          <span>{mode === "promo" ? "THE SPRING EVENT · ENDS SUNDAY" : "NEW SEASON · 2026"}</span>
          <h1>{mode === "promo" ? <>Fresh looks.<br/><em>Better prices.</em></> : <>Everyday pieces,<br/><em>exceptionally chosen.</em></>}</h1>
          <p>{mode === "promo" ? "Save up to 40% across fashion, beauty, home and more. Limited time, unlimited inspiration." : "A thoughtful edit of lasting essentials, new discoveries, and objects that make daily life better."}</p>
          <div className="hero-actions"><Button onClick={() => go("products")}>Shop the collection <Icon name="arrow" size={17}/></Button><Button variant="secondary" onClick={() => go("categories")}>Browse categories</Button></div>
          <div className="hero-meta"><span>4.8/5 from 12k+ reviews</span><span>Free 30-day returns</span></div>
        </div>
        <div className="hero-photo"><img src={PHOTOS.hero} alt="New season fashion collection"/>{mode === "promo" && <div className="offer-bubble"><b>40%</b><span>UP TO<br/>OFF</span></div>}</div>
      </section>

      {mode === "promo" && <div className="promo-strip">
        <div><b>20% OFF BEAUTY</b><span>Glow-up essentials</span><button onClick={() => go("products")}>Shop now</button></div>
        <div><b>MEMBER PRICES</b><span>Extra savings, every day</span><button onClick={() => go("login")}>Join free</button></div>
        <div><b>FLASH DEALS</b><span>New drops every 6 hours</span><button onClick={() => go("products")}>See deals</button></div>
      </div>}

      <Section title="Shop by category" eyebrow={mode === "promo" ? "Find your next favorite" : "Explore the edit"} action={() => go("categories")}>
        <div className="category-grid">{categories.slice(0, 4).map(([name, sub, image]) => <button className="category-card" key={name} onClick={() => go("products")}><img src={image} alt=""/><span><b>{name}</b><small>{sub}</small></span><Icon name="arrow"/></button>)}</div>
      </Section>

      <Section title={mode === "promo" ? "Trending now" : "The considered edit"} eyebrow={mode === "promo" ? "Loved right now" : "Featured"} action={() => go("products")}>
        <div className="product-grid">{products.slice(0, 4).map(p => <ProductCard key={p.id} product={p} go={go} add={add} wish={wish} wished={wishlist.includes(p.id)}/>)}</div>
      </Section>

      {mode === "promo" && <section className="flash">
        <div><span>FLASH DEALS</span><h2>Last chance to save</h2><p>Ends in <b>05 : 42 : 18</b></p><Button onClick={() => go("products")}>Shop all deals</Button></div>
        <div className="flash-products">{products.slice(4).map(p => <ProductCard compact key={p.id} product={p} go={go} add={add} wish={wish} wished={wishlist.includes(p.id)}/>)}</div>
      </section>}

      <Section title={mode === "promo" ? "New drops, just in" : "New & noteworthy"} eyebrow="Fresh arrivals" action={() => go("products")}>
        <div className="editorial">
          <div className="editorial-image"><img src={PHOTOS.fashion2} alt="Relaxed neutral wardrobe"/><div><span>THE WEEKEND EDIT</span><h2>Comfort, considered.</h2><button onClick={() => go("products")}>Discover the collection <Icon name="arrow"/></button></div></div>
          <div className="product-grid two">{products.slice(4, 6).map(p => <ProductCard key={p.id} product={p} go={go} add={add} wish={wish} wished={wishlist.includes(p.id)}/>)}</div>
        </div>
      </Section>

      <div className="benefits"><div><Icon name="truck"/><b>Fast, free delivery</b><span>Free over $75</span></div><div><Icon name="refresh"/><b>Easy returns</b><span>30 days, no stress</span></div><div><Icon name="shield"/><b>Secure payment</b><span>Protected checkout</span></div><div><Icon name="help"/><b>Here to help</b><span>Real support, 7 days</span></div></div>
      <Newsletter/>
    </main>
  </>;
}

function CategoriesPage({ go }: { go: (p: Page) => void }) {
  return <main className="page"><Breadcrumb items={["Categories"]} go={go}/><div className="page-title"><span>DISCOVER</span><h1>Shop by category</h1><p>Explore curated collections across everything you need, want, and love.</p></div>
    <div className="category-page-grid">{categories.map(([name, sub, img], i) => <button key={name} onClick={() => go("products")} className={i < 2 ? "wide" : ""}><img src={img} alt=""/><div><small>{i % 2 ? "80+ BRANDS" : "NEW COLLECTION"}</small><h2>{name}</h2><p>{sub} · {124 + i * 36} products</p><span>Shop now <Icon name="arrow"/></span></div></button>)}</div>
    <Section title="Featured brands" eyebrow="Names to know"><div className="brand-row">{["MORROW", "NORTH STANDARD", "ASTER & MOSS", "SOFT FORM", "ATELIER NO. 8"].map(x => <div key={x}>{x}</div>)}</div></Section>
  </main>;
}

function ProductsPage({ go, add, wish, wishlist, mode }: any) {
  const [sort, setSort] = useState("Recommended");
  const [grid, setGrid] = useState(true);
  const [filters, setFilters] = useState(["In stock", "$50–$150"]);
  const toggle = (x: string) => setFilters((f: string[]) => f.includes(x) ? f.filter(v => v !== x) : [...f, x]);
  return <main className="page"><Breadcrumb items={["Fashion", "All products"]} go={go}/>
    {mode === "promo" && <div className="listing-banner"><div><span>EXTRA 20% OFF</span><h2>Style event</h2><p>Use code STYLE20 at checkout</p></div><img src={PHOTOS.lifestyle} alt="Style event"/></div>}
    <div className="listing-head"><div><span>THE EDIT</span><h1>Fashion & lifestyle</h1><p>342 products</p></div><div className="listing-tools"><button className="filter-mobile"><Icon name="filter"/> Filters</button><select value={sort} onChange={e => setSort(e.target.value)}>{["Recommended", "Popular", "Price: Low to High", "Price: High to Low", "Highest Rated", "Newest"].map(x => <option key={x}>{x}</option>)}</select><button className={grid ? "active" : ""} onClick={() => setGrid(true)}><Icon name="grid"/></button><button className={!grid ? "active" : ""} onClick={() => setGrid(false)}><Icon name="list"/></button></div></div>
    <div className="active-filters">{filters.map((f: string) => <button key={f} onClick={() => toggle(f)}>{f}<Icon name="x" size={13}/></button>)}{filters.length > 0 && <button className="clear" onClick={() => setFilters([])}>Clear all</button>}</div>
    <div className="listing-layout">
      <aside className="filters"><h3>Filters <button onClick={() => setFilters([])}>Clear all</button></h3>
        {[
          ["Category", ["Fashion", "Beauty", "Home & Living", "Accessories"]],
          ["Price range", ["Under $50", "$50–$150", "$150–$300", "$300+"]],
          ["Brand", ["Morrow", "Aster & Moss", "North Standard", "Soft Form"]],
          ["Rating", ["4★ & above", "3★ & above"]],
          ["Availability", ["In stock", "Sale"]],
          ["Size", ["XS", "S", "M", "L", "XL"]],
          ["Color", ["Black", "Ivory", "Sage", "Terracotta"]],
        ].map(([title, opts]) => <div className="filter-group" key={title as string}><h4>{title}</h4>{(opts as string[]).map(x => <label key={x}><input type="checkbox" checked={filters.includes(x)} onChange={() => toggle(x)}/><span>{x}</span><small>{Math.floor(12 + x.length * 7)}</small></label>)}</div>)}
      </aside>
      <div><div className={`product-grid ${grid ? "" : "list-view"}`}>{products.map(p => <ProductCard key={p.id} product={p} go={go} add={add} wish={wish} wished={wishlist.includes(p.id)}/>)}</div><Button variant="secondary" className="load-more">Load more products</Button></div>
    </div>
  </main>;
}

function DetailPage({ go, add, wish, wishlist }: any) {
  const [size, setSize] = useState("M");
  const [color, setColor] = useState("Sand");
  const [qty, setQty] = useState(1);
  const [image, setImage] = useState(PHOTOS.fashion);
  const p = products[0];
  return <main className="page"><Breadcrumb items={["Fashion", "Bags", p.name]} go={go}/>
    <div className="detail">
      <div className="gallery"><div className="thumbs">{[PHOTOS.fashion, PHOTOS.lifestyle, PHOTOS.hero].map((x, i) => <button className={image === x ? "active" : ""} onClick={() => setImage(x)} key={x}><img src={x} alt={`View ${i + 1}`}/></button>)}</div><div className="main-image"><img src={image} alt={p.name}/><span>20% OFF</span></div></div>
      <div className="detail-info"><span className="brand">{p.brand}</span><h1>{p.name}</h1><div className="rating large"><Icon name="star" size={15}/><b>4.8</b><button>248 reviews</button><span>·</span><span>1.2k sold</span></div><div className="detail-price"><strong>$128.00</strong><del>$160.00</del><span>Save $32</span></div><p className="affirm">or 4 interest-free payments of $32.00</p>
        <div className="option"><div><b>Color</b><span>{color}</span></div><div className="swatches">{["Sand", "Ink", "Olive"].map((x, i) => <button aria-label={x} className={`swatch s${i} ${color === x ? "active" : ""}`} onClick={() => setColor(x)} key={x}/>)}</div></div>
        <div className="option"><div><b>Size</b><button>Size guide</button></div><div className="sizes">{["XS", "S", "M", "L", "XL"].map(x => <button className={size === x ? "active" : ""} onClick={() => setSize(x)} key={x}>{x}</button>)}</div></div>
        <div className="buy-row"><div className="qty"><button onClick={() => setQty(Math.max(1, qty - 1))}>−</button><span>{qty}</span><button onClick={() => setQty(qty + 1)}>+</button></div><Button onClick={() => add(p.id)}>Add to cart — ${p.price * qty}</Button><button className={`detail-wish ${wishlist.includes(p.id) ? "active" : ""}`} onClick={() => wish(p.id)}><Icon name="heart"/></button></div>
        <Button className="buy-now" variant="secondary" onClick={() => { add(p.id); go("checkout"); }}>Buy now</Button>
        <div className="delivery-box"><div><Icon name="truck"/><span><b>Delivery to 10001</b><small>Estimated Tue, May 26 · Free</small></span><button>Change</button></div><div><Icon name="refresh"/><span><b>Free 30-day returns</b><small>Easy returns and replacements</small></span></div></div>
        <details open><summary>Product details</summary><p>Designed for everyday versatility, this structured tote features a softly grained finish, secure top closure, internal zip pocket, and adjustable shoulder strap.</p></details><details><summary>Specifications & care</summary><p>Recycled premium textile. 34 × 26 × 12 cm. Wipe clean.</p></details><details><summary>Seller information</summary><p>Sold by Atelier No. 8 · 4.9 seller rating · Ships from New York.</p></details>
      </div>
    </div>
    <Section title="Frequently bought together" eyebrow="Complete the look"><div className="product-grid">{products.slice(1, 5).map(p2 => <ProductCard key={p2.id} product={p2} go={go} add={add} wish={wish} wished={wishlist.includes(p2.id)}/>)}</div></Section>
    <section className="reviews"><div><span>REVIEWS</span><h2>Loved by 248 customers</h2><strong>4.8</strong><div className="stars">★★★★★</div><p>94% would recommend this product</p></div><div>{[["Beautifully made", "The quality is even better in person. It fits my laptop without feeling bulky.", "Maya R."], ["Perfect everyday bag", "The sand color goes with everything and the inside pockets are so useful.", "Jordan K."]].map(r => <article key={r[0]}><div>★★★★★ <span>Verified purchase</span></div><h3>{r[0]}</h3><p>{r[1]}</p><small>{r[2]} · 2 weeks ago</small></article>)}</div></section>
  </main>;
}

function SearchPage({ go, add, wish, wishlist }: any) {
  const [q, setQ] = useState("linen");
  return <main className="page search-page"><Breadcrumb items={["Search"]} go={go}/><div className="search-large"><Icon name="search"/><input autoFocus value={q} onChange={e => setQ(e.target.value)} placeholder="What are you looking for?"/>{q && <button onClick={() => setQ("")}><Icon name="x"/></button>}</div>
    {!q ? <div className="search-empty"><div><h3>Recent searches</h3>{["linen shirt", "skincare set", "travel bag"].map(x => <button onClick={() => setQ(x)} key={x}><Icon name="refresh" size={15}/>{x}</button>)}</div><div><h3>Popular searches</h3>{["New arrivals", "Summer edit", "Gifts under $50", "Bestsellers"].map(x => <button onClick={() => setQ(x)} key={x}>{x}</button>)}</div></div> : q === "xyz" ? <Empty icon="search" title={`No results for “${q}”`} text="Try checking your spelling or using a more general search term." action="Clear search" onClick={() => setQ("")}/> : <><div className="listing-head"><div><span>SEARCH RESULTS</span><h1>Results for “{q}”</h1><p>24 products found</p></div></div><div className="product-grid">{products.slice(0, 4).map(p => <ProductCard key={p.id} product={p} go={go} add={add} wish={wish} wished={wishlist.includes(p.id)}/>)}</div></>}
  </main>;
}

function WishlistPage({ go, add, wish, wishlist }: any) {
  const saved = products.filter(p => wishlist.includes(p.id));
  return <main className="page"><Breadcrumb items={["Wishlist"]} go={go}/><div className="page-title row"><div><span>SAVED FOR LATER</span><h1>My wishlist</h1><p>{saved.length} saved items</p></div></div>
    {saved.length ? <div className="product-grid">{saved.map(p => <ProductCard key={p.id} product={p} go={go} add={add} wish={wish} wished/>)}</div> : <Empty icon="heart" title="Your wishlist is waiting" text="Save pieces you love and come back to them anytime." action="Discover products" onClick={() => go("products")}/>}
  </main>;
}

function CartPage({ go, cart, setCart }: any) {
  const [coupon, setCoupon] = useState("");
  const [applied, setApplied] = useState(false);
  const items = products.filter(p => cart[p.id]);
  const subtotal = items.reduce((s, p) => s + p.price * cart[p.id], 0);
  const update = (id: number, n: number) => setCart({ ...cart, [id]: Math.max(0, n) });
  return <main className="page"><Breadcrumb items={["Shopping cart"]} go={go}/><div className="page-title row"><div><span>YOUR BAG</span><h1>Shopping cart</h1><p>{items.length} items reserved for 20 minutes</p></div></div>
    {!items.length ? <Empty icon="cart" title="Your cart is empty" text="Looks like you haven't added anything yet. Let's change that." action="Start shopping" onClick={() => go("products")}/> :
    <div className="cart-layout"><div className="cart-items">{items.map(p => <article className="cart-item" key={p.id}><img src={p.image} alt=""/><div className="cart-copy"><span>{p.brand}</span><button onClick={() => go("detail")}>{p.name}</button><small>Color: Sand · Size: M</small><div className="stock">In stock · Delivery by Tue, May 26</div><div><button>Save for later</button><button onClick={() => update(p.id, 0)}>Remove</button></div></div><div className="cart-end"><strong>${p.price * cart[p.id]}</strong><del>${p.was * cart[p.id]}</del><div className="qty"><button onClick={() => update(p.id, cart[p.id] - 1)}>−</button><span>{cart[p.id]}</span><button onClick={() => update(p.id, cart[p.id] + 1)}>+</button></div></div></article>)}</div>
      <aside className="summary"><h2>Order summary</h2><label>Promo code</label><div className={`coupon ${coupon && coupon !== "SAVE10" && !applied ? "error" : ""}`}><input value={coupon} onChange={e => {setCoupon(e.target.value.toUpperCase());setApplied(false)}} placeholder="Enter code"/><button onClick={() => coupon === "SAVE10" && setApplied(true)}>Apply</button></div>{coupon && coupon !== "SAVE10" && !applied && <small className="error-text">This code isn't valid. Try SAVE10.</small>}{applied && <div className="success-text"><Icon name="check" size={15}/> SAVE10 applied — you saved $10</div>}
      <div className="totals"><div><span>Subtotal</span><b>${subtotal.toFixed(2)}</b></div><div><span>Product discount</span><b className="saving">−${items.reduce((s,p) => s + (p.was-p.price)*cart[p.id],0).toFixed(2)}</b></div><div><span>Delivery</span><b>FREE</b></div><div><span>Estimated tax</span><b>${(subtotal*.0825).toFixed(2)}</b></div>{applied && <div><span>Coupon</span><b className="saving">−$10.00</b></div>}<div className="total"><span>Total</span><b>${(subtotal*1.0825-(applied?10:0)).toFixed(2)}</b></div></div><Button onClick={() => go("checkout")}>Proceed to checkout <Icon name="arrow"/></Button><p><Icon name="shield" size={15}/> Secure, encrypted checkout</p></aside>
    </div>}
  </main>;
}

function CheckoutPage({ go, cart }: any) {
  const [step, setStep] = useState(1);
  const [payment, setPayment] = useState("card");
  const [processing, setProcessing] = useState(false);
  const next = () => setStep(Math.min(4, step + 1));
  const pay = () => { setProcessing(true); setTimeout(() => { setProcessing(false); go("confirmation"); }, 1400); };
  return <main className="checkout-page"><button className="checkout-logo" onClick={() => go("home")}>MONO<span>MARKET</span></button><div className="checkout-steps">{["Address", "Delivery", "Review", "Payment"].map((x,i) => <div className={step >= i+1 ? "active" : ""} key={x}><span>{step > i+1 ? <Icon name="check" size={15}/> : i+1}</span><b>{x}</b></div>)}</div>
    <div className="checkout-grid"><section className="checkout-main">
      {step === 1 && <><div className="checkout-title"><span>STEP 1 OF 4</span><h1>Where should we deliver?</h1><p>Choose a saved address or add a new one.</p></div><div className="address-grid"><label className="address-card active"><input type="radio" defaultChecked name="address"/><span className="tag">HOME</span><b>Alex Smith</b><p>152 Mercer Street, Apt 4B<br/>New York, NY 10012<br/>United States</p><small>+1 (212) 555-0147</small><div><button>Edit</button><button>Delete</button></div></label><label className="address-card"><input type="radio" name="address"/><span className="tag">WORK</span><b>Alex Smith</b><p>88 Madison Avenue, Floor 6<br/>New York, NY 10016<br/>United States</p><small>+1 (212) 555-0147</small><div><button>Edit</button><button>Delete</button></div></label><button className="add-address">＋<b>Add new address</b><span>Home, work or other</span></button></div></>}
      {step === 2 && <><div className="checkout-title"><span>STEP 2 OF 4</span><h1>Choose delivery method</h1><p>Select the option that works best for you.</p></div><div className="delivery-options">{[["Standard delivery","Tue, May 26 – Wed, May 27","FREE"],["Express delivery","Tomorrow, May 23","$12"],["Scheduled delivery","Choose a date and time","$8"]].map((x,i)=><label className={i===0?"active":""} key={x[0]}><input type="radio" name="delivery" defaultChecked={i===0}/><Icon name="truck"/><span><b>{x[0]}</b><small>{x[1]}</small></span><strong>{x[2]}</strong></label>)}</div></>}
      {step === 3 && <><div className="checkout-title"><span>STEP 3 OF 4</span><h1>Review your order</h1><p>Make sure everything looks right.</p></div><div className="review-block"><h3>Delivery address <button onClick={()=>setStep(1)}>Edit</button></h3><p><b>Alex Smith</b><br/>152 Mercer Street, Apt 4B, New York, NY 10012</p></div><div className="review-block"><h3>Standard delivery <button onClick={()=>setStep(2)}>Edit</button></h3><p>Arrives Tue, May 26 – Wed, May 27 · Free</p></div><div className="review-products">{products.filter(p=>cart[p.id]).map(p=><div key={p.id}><img src={p.image}/><span><b>{p.name}</b><small>Sand / M · Qty {cart[p.id]}</small></span><strong>${p.price*cart[p.id]}</strong></div>)}</div></>}
      {step === 4 && <><div className="checkout-title"><span>STEP 4 OF 4</span><h1>Payment</h1><p>All transactions are secure and encrypted.</p></div><div className="payment-tabs">{[["card","Credit / Debit Card"],["upi","UPI"],["wallet","Wallet"],["bank","Net Banking"],["cod","Cash on Delivery"]].map(x=><button className={payment===x[0]?"active":""} onClick={()=>setPayment(x[0])} key={x[0]}>{x[1]}</button>)}</div>{payment==="card"?<div className="card-form"><label>Card number<input placeholder="1234 5678 9012 3456"/></label><label>Cardholder name<input placeholder="Name on card"/></label><div><label>Expiry date<input placeholder="MM / YY"/></label><label>CVV<input placeholder="•••"/></label></div><label className="save-card"><input type="checkbox"/> Save card securely for future purchases</label></div>:<div className="alt-payment"><Icon name="card" size={36}/><h3>{payment === "upi" ? "Pay with UPI" : payment === "cod" ? "Cash on Delivery" : `Pay with ${payment}`}</h3><p>This is a prototype. No real payment details will be processed.</p></div>}</>}
      <div className="checkout-actions">{step>1&&<Button variant="secondary" onClick={()=>setStep(step-1)}>Back</Button>}<Button onClick={step===4?pay:next} disabled={processing}>{processing?<><span className="spinner"/> Processing payment...</>:step===4?"Pay $276.71":"Continue"}</Button></div>
    </section><OrderMini cart={cart}/></div>
    {processing && <div className="processing-modal"><div><span className="spinner big"/><h2>Processing your payment</h2><p>Please don't close this window or go back.</p><div className="processing-line"><i/></div></div></div>}
  </main>;
}

function OrderMini({cart}:any){const items=products.filter(p=>cart[p.id]);const sub=items.reduce((s,p)=>s+p.price*cart[p.id],0);return <aside className="order-mini"><h3>Your order</h3>{items.map(p=><div className="mini-item" key={p.id}><img src={p.image}/><span><b>{p.name}</b><small>Sand / M · Qty {cart[p.id]}</small></span><strong>${p.price*cart[p.id]}</strong></div>)}<div className="totals"><div><span>Subtotal</span><b>${sub.toFixed(2)}</b></div><div><span>Delivery</span><b>Free</b></div><div><span>Tax</span><b>${(sub*.0825).toFixed(2)}</b></div><div className="total"><span>Total</span><b>${(sub*1.0825).toFixed(2)}</b></div></div><p><Icon name="shield" size={15}/> Secure checkout</p></aside>}

function ConfirmationPage({go}: {go:(p:Page)=>void}) {
  return <main className="page confirmation"><div className="success-icon"><Icon name="check" size={34}/></div><span>ORDER CONFIRMED</span><h1>Thank you, Alex!</h1><p>Your order is confirmed. We’ll send updates to <b>alex.smith@example.com</b>.</p><div className="confirmation-card"><div><span>ORDER ID</span><b>#MM-2026-18429</b></div><div><span>ORDER DATE</span><b>May 22, 2026</b></div><div><span>PAYMENT</span><b>Visa •••• 4242</b></div><div><span>ESTIMATED DELIVERY</span><b>Tue, May 26</b></div></div><div className="confirm-product"><img src={products[0].image}/><span><b>{products[0].name}</b><small>Sand / M · Qty 1</small></span><strong>$128.00</strong></div><div className="confirm-actions"><Button onClick={()=>go("tracking")}>Track order</Button><Button variant="secondary" onClick={()=>go("order-detail")}>View order</Button><Button variant="ghost">Download invoice</Button></div><button className="continue" onClick={()=>go("home")}>Continue shopping <Icon name="arrow"/></button></main>
}

function OrdersPage({go}:{go:(p:Page)=>void}) {
  const [tab,setTab]=useState("All orders");
  return <main className="page"><Breadcrumb items={["Account","My orders"]} go={go}/><div className="account-layout"><AccountNav active="orders" go={go}/><section className="account-content"><div className="page-title"><span>ACCOUNT</span><h1>My orders</h1><p>View, track, and manage your purchases.</p></div><div className="tabs">{["All orders","Active","Delivered","Cancelled","Returned"].map(x=><button className={tab===x?"active":""} onClick={()=>setTab(x)} key={x}>{x}</button>)}</div>{[0,1,2].map((x)=><article className="order-card" key={x}><div className="order-card-head"><div><small>ORDER</small><b>#MM-2026-{18429-x*426}</b></div><div><small>PLACED</small><b>{x?"Apr 18, 2026":"May 22, 2026"}</b></div><div><small>TOTAL</small><b>${x?"86.00":"276.71"}</b></div><span className={x?"delivered":"active"}>{x?"Delivered":"Shipped"}</span></div><div className="order-card-body"><img src={products[x].image}/><span><b>{products[x].name}</b><small>{x?"1 item":"2 items"} · Sand / M</small><small>{x?"Delivered Apr 22":"Arrives Tue, May 26"}</small></span><div><Button variant="secondary" onClick={()=>go("order-detail")}>View details</Button>{!x&&<Button variant="ghost" onClick={()=>go("tracking")}>Track order</Button>}{x>0&&<Button variant="ghost">Buy again</Button>}</div></div></article>)}</section></div></main>
}

function OrderDetailPage({go}:{go:(p:Page)=>void}) {
  return <main className="page"><Breadcrumb items={["My orders","#MM-2026-18429"]} go={go}/><div className="order-detail-head"><div><span>ORDER #MM-2026-18429</span><h1>Order details</h1><p>Placed May 22, 2026 · 2 items</p></div><span className="status-pill">SHIPPED</span></div><div className="order-detail-grid"><section><div className="status-banner"><Icon name="truck"/><span><b>Your order is on the way</b><small>Estimated delivery: Tuesday, May 26</small></span><Button onClick={()=>go("tracking")}>Track order</Button></div>{products.slice(0,2).map(p=><div className="order-line" key={p.id}><img src={p.image}/><span><b>{p.name}</b><small>{p.brand} · Sand / M</small><small>Quantity: 1</small></span><strong>${p.price}</strong></div>)}<div className="order-help"><h3>Need help with this order?</h3><Button variant="secondary">Cancel order</Button><Button variant="ghost">Return / Replace</Button><Button variant="ghost" onClick={()=>go("support")}>Contact support</Button></div></section><aside><div className="info-card"><h3>Delivery address</h3><b>Alex Smith</b><p>152 Mercer Street, Apt 4B<br/>New York, NY 10012</p></div><div className="info-card"><h3>Payment</h3><p>Visa ending in 4242<br/><span>Paid · $276.71</span></p></div><div className="info-card"><h3>Order total</h3><div><span>Subtotal</span><b>$255.00</b></div><div><span>Delivery</span><b>Free</b></div><div><span>Tax</span><b>$21.04</b></div><div><span>Discount</span><b>−$10.00</b></div><div className="total"><span>Total</span><b>$276.71</b></div></div></aside></div></main>
}

function TrackingPage({go}:{go:(p:Page)=>void}) {
  const steps=["Order placed","Confirmed","Packed","Shipped","Out for delivery","Delivered"];
  return <main className="page"><Breadcrumb items={["My orders","#MM-2026-18429","Tracking"]} go={go}/><div className="tracking-head"><span>TRACKING #1Z999AA10123456784</span><h1>Your order is on the way</h1><p>Estimated delivery <b>Tuesday, May 26</b>, between 10am–2pm</p></div><div className="tracking-card"><div className="tracking-visual">{steps.map((x,i)=><div className={i<=3?"complete":""} key={x}><i>{i<3?<Icon name="check" size={15}/>:i===3?<Icon name="truck" size={16}/>:i+1}</i><b>{x}</b><small>{i<=3?["May 22 · 10:42am","May 22 · 11:08am","May 23 · 8:15am","May 24 · 6:30am"][i]:"Pending"}</small></div>)}</div><div className="tracking-update"><span>Latest update</span><h3>Departed carrier facility</h3><p>Newark, NJ · May 24 at 6:30am</p></div></div><div className="tracking-bottom"><div className="confirm-product"><img src={products[0].image}/><span><b>{products[0].name}</b><small>Order #MM-2026-18429 · 2 items</small></span><Button variant="secondary" onClick={()=>go("order-detail")}>View order</Button></div><div className="info-card"><h3>Delivery address</h3><p>152 Mercer Street, Apt 4B<br/>New York, NY 10012</p><button>Delivery instructions</button></div></div></main>
}

function ProfilePage({go}:{go:(p:Page)=>void}) {
  return <main className="page"><Breadcrumb items={["Account"]} go={go}/><div className="account-layout"><AccountNav active="profile" go={go}/><section className="account-content"><div className="profile-hero"><span>AS</span><div><h1>Alex Smith</h1><p>alex.smith@example.com · Member since 2024</p></div><Button variant="secondary">Edit profile</Button></div><div className="account-stats"><button onClick={()=>go("orders")}><b>12</b><span>Total orders</span></button><button onClick={()=>go("wishlist")}><b>4</b><span>Wishlist items</span></button><button><b>2</b><span>Saved addresses</span></button></div><h2 className="account-section-title">Account settings</h2><div className="settings-grid">{[["user","Personal information","Name, email and phone"],["home","Saved addresses","Home, work and other"],["card","Payment methods","Cards and wallets"],["bell","Notifications","Your communication preferences"],["shield","Security","Password and sign-in"],["help","Help & support","FAQs and contact options"]].map(x=><button onClick={()=>x[0]==="bell"?go("notifications"):x[0]==="help"?go("support"):undefined} key={x[1]}><Icon name={x[0] as IconName}/><span><b>{x[1]}</b><small>{x[2]}</small></span><Icon name="chevron"/></button>)}</div></section></div></main>
}

function AccountNav({active,go}:{active:string;go:(p:Page)=>void}){return <aside className="account-nav"><h3>My account</h3>{[["profile","user","Overview"],["orders","package","My orders"],["wishlist","heart","Wishlist"],["addresses","home","Saved addresses"],["payment","card","Payment methods"],["notifications","bell","Notifications"],["support","help","Help & support"]].map(x=><button className={active===x[0]?"active":""} onClick={()=>x[0]==="orders"?go("orders"):x[0]==="wishlist"?go("wishlist"):x[0]==="notifications"?go("notifications"):x[0]==="support"?go("support"):go("profile")} key={x[0]}><Icon name={x[1] as IconName}/>{x[2]}<Icon name="chevron" size={14}/></button>)}<button className="logout"><Icon name="logout"/>Log out</button></aside>}

function NotificationsPage({go}:{go:(p:Page)=>void}) {
  const [read,setRead]=useState<number[]>([2,3]);
  return <main className="page"><Breadcrumb items={["Account","Notifications"]} go={go}/><div className="account-layout"><AccountNav active="notifications" go={go}/><section className="account-content"><div className="page-title row"><div><span>UPDATES</span><h1>Notifications</h1><p>Stay up to date with orders and offers.</p></div><button onClick={()=>setRead([0,1,2,3,4])}>Mark all as read</button></div><div className="tabs"><button className="active">All</button><button>Orders</button><button>Offers</button></div><div className="notification-list">{[["truck","Your order has shipped","Order #MM-2026-18429 is on its way. Track your delivery for the latest updates.","2 hours ago"],["card","Payment confirmed","Your payment of $276.71 was successful.","Yesterday"],["package","Delivered successfully","Your Aster & Moss order was delivered.","Apr 22"],["heart","Price drop on a saved item","The Cloud Cotton Lounge Set is now 22% off.","Apr 20"],["bell","Just for you: 20% off beauty","Use GLOW20 on selected beauty essentials through Sunday.","Apr 18"]].map((n,i)=><button className={read.includes(i)?"read":""} onClick={()=>setRead([...read,i])} key={n[1]}><i><Icon name={n[0] as IconName}/></i><span><b>{n[1]}</b><p>{n[2]}</p><small>{n[3]}</small></span>{!read.includes(i)&&<em/>}</button>)}</div></section></div></main>
}

function SupportPage({go}:{go:(p:Page)=>void}) {
  const [open,setOpen]=useState(0);
  return <main className="page support"><Breadcrumb items={["Help & support"]} go={go}/><div className="support-hero"><span>HOW CAN WE HELP?</span><h1>Help center</h1><div><Icon name="search"/><input placeholder="Search orders, returns, payments..."/></div><p>Popular: <button>track my order</button> <button>start a return</button> <button>payment help</button></p></div><div className="help-grid">{[["package","Order help","Track, change or cancel"],["refresh","Returns & refunds","Start or check a return"],["card","Payment help","Charges and payment issues"],["truck","Delivery help","Shipping and delivery"],["user","Account help","Profile, login and security"],["help","Contact support","Chat or send a message"]].map(x=><button key={x[1]}><Icon name={x[0] as IconName}/><b>{x[1]}</b><span>{x[2]}</span><Icon name="chevron"/></button>)}</div><section className="faq"><span>FREQUENTLY ASKED</span><h2>Quick answers</h2>{["Where is my order?","How do I return or replace an item?","When will I receive my refund?","Can I change my delivery address?","What payment methods do you accept?"].map((x,i)=><article key={x}><button onClick={()=>setOpen(open===i?-1:i)}><b>{x}</b><span>{open===i?"−":"+"}</span></button>{open===i&&<p>You can manage this from My Orders. Select the relevant order and choose the available action. If you still need help, our support team is available every day from 8am–10pm.</p>}</article>)}</section></main>
}

function LoginPage({go}:{go:(p:Page)=>void}) {
  const [register,setRegister]=useState(false);
  return <main className="auth"><div className="auth-photo"><img src={PHOTOS.hero}/><div><span>MONOMARKET</span><h1>Good choices,<br/>made simple.</h1><p>Discover thoughtful products from brands worth knowing.</p></div></div><div className="auth-form"><button className="logo" onClick={()=>go("home")}>MONO<span>MARKET</span></button><div><span>{register?"JOIN MONOMARKET":"WELCOME BACK"}</span><h1>{register?"Create an account":"Sign in to your account"}</h1><p>{register?"Already have an account?":"New here?"} <button onClick={()=>setRegister(!register)}>{register?"Sign in":"Create an account"}</button></p>{register&&<label>Full name<input placeholder="Alex Smith"/></label>}<label>Email address<input type="email" placeholder="alex@example.com"/></label><label>Password<input type="password" placeholder="At least 8 characters"/></label><div className="auth-options"><label><input type="checkbox"/>Remember me</label><button>Forgot password?</button></div><Button onClick={()=>go("home")}>{register?"Create account":"Sign in"}</Button><div className="or"><span/>OR CONTINUE WITH<span/></div><div className="social-login"><Button variant="secondary">Google</Button><Button variant="secondary">Apple</Button></div><small>By continuing, you agree to our Terms and Privacy Policy.</small></div></div></main>
}

function Empty({icon,title,text,action,onClick}:{icon:IconName;title:string;text:string;action:string;onClick:()=>void}){return <div className="empty"><i><Icon name={icon} size={34}/></i><h2>{title}</h2><p>{text}</p><Button onClick={onClick}>{action}</Button></div>}
function Newsletter(){return <section className="newsletter"><span>THE GOOD STUFF, DELIVERED</span><h2>Join our thoughtful little list.</h2><p>New arrivals, considered edits, and occasional treats. No noise.</p><div><input type="email" placeholder="Your email address"/><button>Subscribe <Icon name="arrow"/></button></div><small>By subscribing, you agree to our Privacy Policy.</small></section>}
function Footer({go}:{go:(p:Page)=>void}){return <footer><div className="footer-main"><div className="footer-brand"><button className="logo" onClick={()=>go("home")}>MONO<span>MARKET</span></button><p>Thoughtful products for a life well lived. Selected with care, delivered with ease.</p><div className="socials"><button>IG</button><button>PI</button><button>TT</button></div></div>{[["Shop",["New arrivals","Bestsellers","Deals","Gift cards"]],["Help",["Help center","Delivery","Returns & refunds","Contact us"]],["About",["Our story","Careers","Responsibility","Journal"]],["Legal",["Privacy policy","Terms & conditions","Shipping policy","Refund policy"]]].map(c=><div key={c[0]}><b>{c[0]}</b>{c[1].map(x=><button onClick={()=>x==="Help center"&&go("support")} key={x}>{x}</button>)}</div>)}</div><div className="footer-bottom"><span>© 2026 MonoMarket. All rights reserved.</span><span>United States · USD $</span></div></footer>}

export default function App() {
  const [page, setPage] = useState<Page>("home");
  const [mode, setMode] = useState<"minimal" | "promo">("minimal");
  const [wishlist, setWishlist] = useState<number[]>([2, 4]);
  const [cart, setCart] = useState<Record<number,number>>({ 1: 1, 2: 1 });
  const [toast, setToast] = useState("");
  const cartCount = useMemo(() => Object.values(cart).reduce((a,b)=>a+b,0), [cart]);
  const go = (p: Page) => { setPage(p); window.scrollTo({top:0, behavior:"smooth"}); };
  const add = (id:number) => { setCart(c=>({...c,[id]:(c[id]||0)+1})); setToast("Added to your cart"); setTimeout(()=>setToast(""),2200); };
  const wish = (id:number) => { setWishlist(w=>w.includes(id)?w.filter(x=>x!==id):[...w,id]); setToast(wishlist.includes(id)?"Removed from wishlist":"Saved to your wishlist"); setTimeout(()=>setToast(""),2200); };
  const shared={go,add,wish,wishlist};
  const standalone = page === "checkout" || page === "login";
  return <div className={`app mode-${mode}`}>
    {!standalone && <Header go={go} cartCount={cartCount} mode={mode} setMode={setMode}/>}
    {page==="home"&&<HomePage {...shared} mode={mode}/>}
    {page==="categories"&&<CategoriesPage go={go}/>}
    {page==="products"&&<ProductsPage {...shared} mode={mode}/>}
    {page==="detail"&&<DetailPage {...shared}/>}
    {page==="search"&&<SearchPage {...shared}/>}
    {page==="wishlist"&&<WishlistPage {...shared}/>}
    {page==="cart"&&<CartPage go={go} cart={cart} setCart={setCart}/>}
    {page==="checkout"&&<CheckoutPage go={go} cart={cart}/>}
    {page==="confirmation"&&<ConfirmationPage go={go}/>}
    {page==="orders"&&<OrdersPage go={go}/>}
    {page==="order-detail"&&<OrderDetailPage go={go}/>}
    {page==="tracking"&&<TrackingPage go={go}/>}
    {page==="profile"&&<ProfilePage go={go}/>}
    {page==="notifications"&&<NotificationsPage go={go}/>}
    {page==="support"&&<SupportPage go={go}/>}
    {page==="login"&&<LoginPage go={go}/>}
    {!standalone && <Footer go={go}/>}
    {toast&&<div className="toast"><Icon name="check"/><span>{toast}</span><button onClick={()=>setToast("")}><Icon name="x" size={16}/></button></div>}
    {!standalone&&<nav className="mobile-bottom"><button onClick={()=>go("home")}><Icon name="home"/><span>Home</span></button><button onClick={()=>go("products")}><Icon name="search"/><span>Shop</span></button><button onClick={()=>go("wishlist")}><Icon name="heart"/><span>Saved</span></button><button onClick={()=>go("cart")}><Icon name="cart"/><span>Cart</span></button><button onClick={()=>go("profile")}><Icon name="user"/><span>Account</span></button></nav>}
  </div>;
}

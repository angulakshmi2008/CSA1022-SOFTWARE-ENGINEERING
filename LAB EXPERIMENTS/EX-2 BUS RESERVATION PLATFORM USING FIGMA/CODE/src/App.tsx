import { useMemo, useState, type ReactNode } from "react";

type Page =
  | "dashboard"
  | "buses"
  | "seats"
  | "details"
  | "payment"
  | "confirmed"
  | "ticket"
  | "bookings"
  | "track";

type Bus = {
  id: string;
  name: string;
  registration: string;
  type: string;
  seatType: string;
  layout: "sleeper" | "seater";
  departure: string;
  arrival: string;
  duration: string;
  fare: number;
  available: number;
  accent: string;
};

const buses: Bus[] = [
  {
    id: "sleep",
    name: "GreenLine Night Rider",
    registration: "KA 01 AB 4582",
    type: "A/C Sleeper",
    seatType: "Single & Double Berths",
    layout: "sleeper",
    departure: "21:30",
    arrival: "06:15",
    duration: "8h 45m",
    fare: 1299,
    available: 21,
    accent: "#4f46e5",
  },
  {
    id: "seat",
    name: "CityLink Express",
    registration: "TS 09 UA 7321",
    type: "Volvo A/C Seater",
    seatType: "Reclining 2+2 Seats",
    layout: "seater",
    departure: "22:45",
    arrival: "07:30",
    duration: "8h 45m",
    fare: 849,
    available: 38,
    accent: "#0891b2",
  },
  {
    id: "srs-sleeper",
    name: "SRS Royal Cruiser",
    registration: "KA 51 AC 9087",
    type: "Volvo Multi-Axle Sleeper",
    seatType: "Premium A/C Berths",
    layout: "sleeper",
    departure: "19:45",
    arrival: "04:50",
    duration: "9h 05m",
    fare: 1499,
    available: 17,
    accent: "#dc2626",
  },
  {
    id: "orange-seater",
    name: "Orange Tours & Travels",
    registration: "TS 08 UF 6140",
    type: "Mercedes A/C Seater",
    seatType: "Reclining 2+2 Seats",
    layout: "seater",
    departure: "20:15",
    arrival: "05:25",
    duration: "9h 10m",
    fare: 999,
    available: 31,
    accent: "#ea580c",
  },
  {
    id: "ksrtc-sleeper",
    name: "KSRTC Airavat Club Class",
    registration: "KA 57 F 3128",
    type: "A/C Sleeper",
    seatType: "Airavat Premium Berths",
    layout: "sleeper",
    departure: "22:10",
    arrival: "07:05",
    duration: "8h 55m",
    fare: 1375,
    available: 12,
    accent: "#166534",
  },
  {
    id: "intrcity-seater",
    name: "IntrCity SmartBus",
    registration: "HR 55 AN 2046",
    type: "BharatBenz A/C Seater",
    seatType: "Smart Reclining Seats",
    layout: "seater",
    departure: "18:30",
    arrival: "03:45",
    duration: "9h 15m",
    fare: 799,
    available: 42,
    accent: "#7c3aed",
  },
  {
    id: "vrdl-sleeper",
    name: "VRL Travels",
    registration: "KA 25 D 8824",
    type: "A/C Multi-Axle Sleeper",
    seatType: "Luxury Berths",
    layout: "sleeper",
    departure: "23:15",
    arrival: "08:00",
    duration: "8h 45m",
    fare: 1199,
    available: 24,
    accent: "#ca8a04",
  },
  {
    id: "zing-seater",
    name: "Zingbus Premium",
    registration: "DL 01 PC 7692",
    type: "Volvo A/C Seater",
    seatType: "Premium Reclining 2+2",
    layout: "seater",
    departure: "17:50",
    arrival: "03:10",
    duration: "9h 20m",
    fare: 749,
    available: 36,
    accent: "#2563eb",
  },
];

const sleeperReserved = new Set(["U03", "U07", "U11", "U14", "L02", "L06", "L09", "L13", "L15"]);
const seaterReserved = new Set(["1A", "1D", "2B", "3C", "4A", "4D", "5B", "6C", "7A", "8D", "9B", "10C", "11A", "12D"]);

const indianLocations: Record<string, string[]> = {
  "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Tirupati", "Guntur", "Nellore"],
  Assam: ["Guwahati", "Dibrugarh", "Silchar"],
  Bihar: ["Patna", "Gaya", "Muzaffarpur"],
  Delhi: ["New Delhi"],
  Goa: ["Panaji", "Margao", "Vasco da Gama"],
  Gujarat: ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
  Haryana: ["Gurugram", "Faridabad", "Panipat"],
  "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
  Jharkhand: ["Ranchi", "Jamshedpur", "Dhanbad"],
  Karnataka: ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi"],
  Kerala: ["Kochi", "Thiruvananthapuram", "Kozhikode", "Thrissur"],
  "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior"],
  Maharashtra: ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
  Odisha: ["Bhubaneswar", "Cuttack", "Rourkela"],
  Punjab: ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar"],
  Rajasthan: ["Jaipur", "Udaipur", "Jodhpur", "Kota"],
  "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Tiruchirappalli"],
  Telangana: ["Hyderabad", "Warangal", "Karimnagar"],
  "Uttar Pradesh": ["Lucknow", "Varanasi", "Agra", "Kanpur", "Noida"],
  Uttarakhand: ["Dehradun", "Haridwar", "Rishikesh"],
  "West Bengal": ["Kolkata", "Siliguri", "Durgapur"],
};

const stateForCity = (city: string) =>
  Object.entries(indianLocations).find(([, cities]) => cities.includes(city))?.[0] ?? "India";

function LocationOptions() {
  return (
    <>
      {Object.entries(indianLocations).map(([state, cities]) => (
        <optgroup key={state} label={state}>
          {cities.map((city) => <option key={city} value={city}>{city}</option>)}
        </optgroup>
      ))}
    </>
  );
}

const Icon = ({ name, size = 20 }: { name: string; size?: number }) => {
  const paths: Record<string, ReactNode> = {
    bus: <><rect x="5" y="3" width="14" height="16" rx="3" /><path d="M5 12h14M8 7h8M8 19v2m8-2v2M8.5 16h.01m7-.01h.01" /></>,
    route: <><circle cx="6" cy="6" r="2" /><circle cx="18" cy="18" r="2" /><path d="M8 6h4a3 3 0 0 1 3 3v6a3 3 0 0 0 3 3" /></>,
    ticket: <><path d="M4 6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v3a3 3 0 0 0 0 6v3a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-3a3 3 0 0 0 0-6Z" /><path d="M13 7v2m0 3v1m0 3v1" /></>,
    user: <><circle cx="12" cy="8" r="4" /><path d="M4 21a8 8 0 0 1 16 0" /></>,
    calendar: <><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M16 3v4M8 3v4M3 10h18" /></>,
    swap: <><path d="m7 7-3 3 3 3M4 10h16M17 17l3-3-3-3M20 14H4" /></>,
    arrow: <path d="m9 18 6-6-6-6" />,
    back: <path d="m15 18-6-6 6-6" />,
    pin: <><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z" /><circle cx="12" cy="10" r="2.5" /></>,
    clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
    seat: <><path d="M7 12V6a3 3 0 0 1 6 0v6M5 10a2 2 0 0 0-2 2v4a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-4a2 2 0 0 0-2-2" /><path d="M7 15h10M6 19v2m12-2v2" /></>,
    check: <path d="m5 12 4 4L19 6" />,
    card: <><rect x="3" y="5" width="18" height="14" rx="2" /><path d="M3 10h18M7 15h3" /></>,
    shield: <><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" /><path d="m9 12 2 2 4-4" /></>,
    download: <><path d="M12 3v12m0 0 4-4m-4 4-4-4M5 21h14" /></>,
    logout: <><path d="M10 17l5-5-5-5M15 12H3M15 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4" /></>,
    wallet: <><path d="M4 6h14a2 2 0 0 1 2 2v10H4a2 2 0 0 1-2-2V6a3 3 0 0 1 3-3h12" /><path d="M15 11h7v4h-7a2 2 0 0 1 0-4Z" /></>,
  };
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      {paths[name]}
    </svg>
  );
};

function Button({
  children,
  onClick,
  variant = "primary",
  className = "",
  disabled = false,
}: {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "ghost";
  className?: string;
  disabled?: boolean;
}) {
  return (
    <button onClick={onClick} disabled={disabled} className={`btn btn-${variant} ${className}`}>
      {children}
    </button>
  );
}

function App() {
  const [page, setPage] = useState<Page>("dashboard");
  const [source, setSource] = useState("Bengaluru");
  const [destination, setDestination] = useState("Hyderabad");
  const [date, setDate] = useState("2025-08-22");
  const [passengers, setPassengers] = useState(1);
  const [selectedBus, setSelectedBus] = useState<Bus>(buses[0]);
  const [selectedSeat, setSelectedSeat] = useState("");
  const [deck, setDeck] = useState<"upper" | "lower">("lower");
  const [boarding, setBoarding] = useState("Majestic Bus Station — 21:00");
  const [dropping, setDropping] = useState("MGBS, Hyderabad — 06:15");
  const [payment, setPayment] = useState("upi");
  const [mobileMenu, setMobileMenu] = useState(false);

  const formattedDate = useMemo(
    () => new Date(`${date}T12:00:00`).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" }),
    [date],
  );

  const navigate = (next: Page) => {
    setPage(next);
    setMobileMenu(false);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const swap = () => {
    setSource(destination);
    setDestination(source);
  };

  const openSeats = (bus: Bus) => {
    setSelectedBus(bus);
    setSelectedSeat("");
    setDeck("lower");
    navigate("seats");
  };

  const navItems: { label: string; page: Page; icon: string }[] = [
    { label: "Book a trip", page: "dashboard", icon: "route" },
    { label: "My bookings", page: "bookings", icon: "ticket" },
    { label: "Track bus", page: "track", icon: "pin" },
  ];

  return (
    <div className="app-shell">
      <header className="header">
        <button className="brand" onClick={() => navigate("dashboard")} aria-label="Go to dashboard">
          <span className="brand-mark"><Icon name="bus" size={23} /></span>
          <span>Via<span>Route</span></span>
        </button>
        <nav className="desktop-nav">
          {navItems.map((item) => (
            <button key={item.page} className={page === item.page ? "active" : ""} onClick={() => navigate(item.page)}>
              {item.label}
            </button>
          ))}
        </nav>
        <div className="header-actions">
          <button className="profile-button"><span>AK</span><span className="profile-copy"><b>Arjun Kumar</b><small>Explorer</small></span></button>
          <button className="menu-button" onClick={() => setMobileMenu(!mobileMenu)} aria-label="Toggle menu">
            <span /><span /><span />
          </button>
        </div>
        {mobileMenu && (
          <div className="mobile-nav">
            {navItems.map((item) => (
              <button key={item.page} onClick={() => navigate(item.page)}><Icon name={item.icon} />{item.label}</button>
            ))}
          </div>
        )}
      </header>

      <main>
        {page === "dashboard" && (
          <Dashboard
            source={source}
            destination={destination}
            date={date}
            passengers={passengers}
            setSource={setSource}
            setDestination={setDestination}
            setDate={setDate}
            setPassengers={setPassengers}
            swap={swap}
            search={() => navigate("buses")}
          />
        )}
        {page === "buses" && <BusList source={source} destination={destination} date={formattedDate} passengers={passengers} onBack={() => navigate("dashboard")} onSeats={openSeats} />}
        {page === "seats" && <SeatSelection bus={selectedBus} deck={deck} setDeck={setDeck} selected={selectedSeat} setSelected={setSelectedSeat} onBack={() => navigate("buses")} onContinue={() => navigate("details")} />}
        {page === "details" && <BookingDetails bus={selectedBus} source={source} destination={destination} date={formattedDate} selected={selectedSeat} boarding={boarding} dropping={dropping} setBoarding={setBoarding} setDropping={setDropping} onBack={() => navigate("seats")} onContinue={() => navigate("payment")} />}
        {page === "payment" && <Payment bus={selectedBus} selected={selectedSeat} method={payment} setMethod={setPayment} onBack={() => navigate("details")} onPay={() => navigate("confirmed")} />}
        {page === "confirmed" && <Confirmed bus={selectedBus} source={source} destination={destination} date={formattedDate} selected={selectedSeat} onTicket={() => navigate("ticket")} onHome={() => navigate("dashboard")} />}
        {page === "ticket" && <DigitalTicket bus={selectedBus} source={source} destination={destination} date={formattedDate} selected={selectedSeat} boarding={boarding} dropping={dropping} onHome={() => navigate("dashboard")} />}
        {page === "bookings" && <MyBookings onTicket={() => navigate("ticket")} onTrack={() => navigate("track")} />}
        {page === "track" && <TrackBus source={source} destination={destination} onBack={() => navigate("dashboard")} />}
      </main>

      <footer>
        <div className="footer-brand"><span className="brand-mark"><Icon name="bus" size={19} /></span><b>ViaRoute</b></div>
        <p>Safe journeys, thoughtfully planned.</p>
        <span>© 2025 ViaRoute</span>
      </footer>
    </div>
  );
}

function Dashboard({ source, destination, date, passengers, setSource, setDestination, setDate, setPassengers, swap, search }: {
  source: string; destination: string; date: string; passengers: number;
  setSource: (v: string) => void; setDestination: (v: string) => void; setDate: (v: string) => void; setPassengers: (v: number) => void; swap: () => void; search: () => void;
}) {
  return (
    <>
      <section className="hero">
        <div className="hero-orb orb-one" /><div className="hero-orb orb-two" />
        <div className="hero-copy">
          <span className="eyebrow light">SMARTER INTERCITY TRAVEL</span>
          <h1>Your journey.<br /><em>Beautifully simple.</em></h1>
          <p>Find the right bus, choose your favourite seat, and travel with confidence.</p>
          <div className="trust-row"><span><Icon name="shield" size={17} /> Verified operators</span><span><Icon name="ticket" size={17} /> Instant confirmation</span></div>
        </div>
        <div className="search-card">
          <div className="search-card-heading"><span><Icon name="route" /></span><div><small>PLAN YOUR TRIP</small><h2>Where are you going?</h2></div></div>
          <div className="route-fields">
            <label><span>FROM</span><div><i className="dot source-dot" /><select value={source} onChange={(e) => setSource(e.target.value)}><LocationOptions /></select></div><small>{stateForCity(source)}, India</small></label>
            <button className="swap-button" onClick={swap} aria-label="Swap source and destination"><Icon name="swap" /></button>
            <label><span>TO</span><div><i className="dot destination-dot" /><select value={destination} onChange={(e) => setDestination(e.target.value)}><LocationOptions /></select></div><small>{stateForCity(destination)}, India</small></label>
          </div>
          <div className="trip-fields">
            <label><span>TRAVEL DATE</span><div><Icon name="calendar" /><input type="date" value={date} onChange={(e) => setDate(e.target.value)} /></div></label>
            <label><span>PASSENGERS</span><div><Icon name="user" /><select value={passengers} onChange={(e) => setPassengers(Number(e.target.value))}><option value={1}>1 Passenger</option><option value={2}>2 Passengers</option><option value={3}>3 Passengers</option><option value={4}>4 Passengers</option></select></div></label>
          </div>
          <Button onClick={search} className="search-button">Search buses <Icon name="arrow" /></Button>
          <p className="safe-note"><Icon name="shield" size={15} /> Secure booking · No hidden charges</p>
        </div>
      </section>
      <section className="benefits">
        <div><span><Icon name="seat" /></span><div><b>Choose your exact seat</b><p>See real-time seat availability</p></div></div>
        <div><span><Icon name="wallet" /></span><div><b>Transparent pricing</b><p>What you see is what you pay</p></div></div>
        <div><span><Icon name="pin" /></span><div><b>Track your bus live</b><p>Real-time location updates</p></div></div>
      </section>
    </>
  );
}

function PageTop({ label, title, subtitle, onBack }: { label: string; title: string; subtitle?: string; onBack?: () => void }) {
  return (
    <div className="page-top">
      {onBack && <button className="back-button" onClick={onBack}><Icon name="back" /> Back</button>}
      <span className="eyebrow">{label}</span>
      <h1>{title}</h1>
      {subtitle && <p>{subtitle}</p>}
    </div>
  );
}

function BusList({ source, destination, date, passengers, onBack, onSeats }: { source: string; destination: string; date: string; passengers: number; onBack: () => void; onSeats: (bus: Bus) => void }) {
  return (
    <div className="page-wrap">
      <PageTop label="AVAILABLE JOURNEYS" title={`${source} to ${destination}`} subtitle={`${date} · ${passengers} passenger${passengers > 1 ? "s" : ""}`} onBack={onBack} />
      <div className="list-toolbar"><p><b>{buses.length} buses</b> found for your route</p><select aria-label="Sort buses"><option>Sort: Recommended</option><option>Fare: Low to high</option><option>Departure time</option></select></div>
      <div className="bus-list">
        {buses.map((bus, index) => (
          <article className="bus-card" key={bus.id}>
            <div className="bus-main">
              <div className="bus-identity"><span className="bus-icon" style={{ background: bus.accent }}><Icon name="bus" /></span><div><div className="operator-line"><h2>{bus.name}</h2>{index === 0 && <span className="recommended">RECOMMENDED</span>}</div><p>{bus.registration} · {bus.type} · {bus.seatType}</p><div className="rating"><b>{index === 0 ? "4.8" : (4.3 + (index % 5) * 0.1).toFixed(1)}</b> <span>★★★★★</span> <small>{index === 0 ? "1,240" : 520 + index * 84} ratings</small></div></div></div>
              <div className="time-line">
                <div><b>{bus.departure}</b><small>{source}</small></div>
                <div className="duration"><span>{bus.duration}</span><i><em /></i><small>Overnight</small></div>
                <div><b>{bus.arrival}</b><small>{destination}</small></div>
              </div>
            </div>
            <div className="amenities"><span>AC</span><span>Charging port</span><span>Water bottle</span><span>Live tracking</span></div>
            <div className="bus-price"><small>Starting from</small><strong>₹{bus.fare.toLocaleString("en-IN")}</strong><span>{bus.available} seats available</span><Button onClick={() => onSeats(bus)}>View seats <Icon name="arrow" /></Button></div>
          </article>
        ))}
      </div>
    </div>
  );
}

function Legend() {
  return <div className="legend"><span><i className="available" />Available</span><span><i className="selected" />Selected</span><span><i className="reserved" />Reserved</span></div>;
}

function SeatSelection({ bus, deck, setDeck, selected, setSelected, onBack, onContinue }: { bus: Bus; deck: "upper" | "lower"; setDeck: (v: "upper" | "lower") => void; selected: string; setSelected: (v: string) => void; onBack: () => void; onContinue: () => void }) {
  const isSleeper = bus.layout === "sleeper";
  return (
    <div className="page-wrap">
      <PageTop label="SELECT YOUR PLACE" title={isSleeper ? "Choose your berth" : "Choose your seat"} subtitle={`${bus.name} · ${bus.type}`} onBack={onBack} />
      <div className="seat-page-grid">
        <section className="layout-card">
          <div className="layout-header"><div><h2>{isSleeper ? "Sleeper coach" : "Reclining seater coach"}</h2><p>{isSleeper ? "30 berths · 15 on each deck" : "52 reclining seats · 2+2 layout"}</p></div><Legend /></div>
          {isSleeper ? (
            <>
              <div className="deck-tabs"><button className={deck === "lower" ? "active" : ""} onClick={() => setDeck("lower")}>Lower deck <span>15 berths</span></button><button className={deck === "upper" ? "active" : ""} onClick={() => setDeck("upper")}>Upper deck <span>15 berths</span></button></div>
              <SleeperLayout deck={deck} selected={selected} setSelected={setSelected} />
            </>
          ) : <SeaterLayout selected={selected} setSelected={setSelected} />}
        </section>
        <aside className="selection-summary">
          <span className="summary-icon"><Icon name="seat" /></span>
          <h3>{selected ? "Great choice" : "Select a seat"}</h3>
          <p>{selected ? `Your ${isSleeper ? "berth" : "seat"} is held for 10 minutes.` : `Choose any available ${isSleeper ? "berth" : "seat"} from the layout.`}</p>
          <div className="summary-row"><span>Selected</span><b>{selected || "—"}</b></div>
          <div className="summary-row"><span>Seat fare</span><b>{selected ? `₹${bus.fare.toLocaleString("en-IN")}` : "₹0"}</b></div>
          <div className="summary-total"><span>Total</span><strong>{selected ? `₹${bus.fare.toLocaleString("en-IN")}` : "₹0"}</strong></div>
          <Button disabled={!selected} onClick={onContinue} className="full-button">Continue to booking <Icon name="arrow" /></Button>
          <small className="center-note"><Icon name="shield" size={14} /> Free cancellation within 30 minutes</small>
        </aside>
      </div>
    </div>
  );
}

function SleeperLayout({ deck, selected, setSelected }: { deck: "upper" | "lower"; selected: string; setSelected: (v: string) => void }) {
  const prefix = deck === "upper" ? "U" : "L";
  const berths = Array.from({ length: 15 }, (_, i) => `${prefix}${String(i + 1).padStart(2, "0")}`);
  return (
    <div className="coach sleeper-coach">
      <div className="coach-front"><span>FRONT</span><Icon name="bus" /></div>
      <div className="berth-grid">
        {berths.map((berth) => {
          const reserved = sleeperReserved.has(berth);
          return <button key={berth} disabled={reserved} onClick={() => setSelected(berth)} className={`berth ${reserved ? "reserved" : selected === berth ? "selected" : ""}`}><i /><b>{berth}</b><small>{reserved ? "Booked" : selected === berth ? "Selected" : "Available"}</small></button>;
        })}
      </div>
      <p className="coach-hint">Each deck has exactly 15 full-length berths</p>
    </div>
  );
}

function SeaterLayout({ selected, setSelected }: { selected: string; setSelected: (v: string) => void }) {
  const seats = Array.from({ length: 13 }, (_, row) => ["A", "B", "C", "D"].map((letter) => `${row + 1}${letter}`));
  return (
    <div className="coach seater-coach">
      <div className="driver"><span>FRONT</span><div>◯</div></div>
      <div className="seat-labels"><span>WINDOW</span><span>AISLE</span><span>AISLE</span><span>WINDOW</span></div>
      <div className="seat-grid">
        {seats.flat().map((seat) => {
          const reserved = seaterReserved.has(seat);
          const aisleGap = seat.endsWith("C");
          return <button title={`${seat.endsWith("A") || seat.endsWith("D") ? "Window" : "Aisle"} reclining seat`} style={aisleGap ? { marginLeft: 30 } : undefined} key={seat} disabled={reserved} onClick={() => setSelected(seat)} className={`seat ${reserved ? "reserved" : selected === seat ? "selected" : ""}`}><Icon name="seat" size={21} /><b>{seat}</b><small>R</small></button>;
        })}
      </div>
      <p className="coach-hint"><b>R</b> indicates a reclining seat · 52 seats total</p>
    </div>
  );
}

function TripSummary({ bus, source, destination, date, selected }: { bus: Bus; source: string; destination: string; date: string; selected: string }) {
  return (
    <aside className="trip-summary">
      <span className="eyebrow">YOUR JOURNEY</span>
      <h3>{source} <Icon name="arrow" size={16} /> {destination}</h3>
      <p>{date}</p>
      <div className="mini-route"><div><i /><span><b>{bus.departure}</b><small>{source}</small></span></div><em /><div><i /><span><b>{bus.arrival}</b><small>{destination}</small></span></div></div>
      <div className="summary-row"><span>Bus</span><b>{bus.name}</b></div>
      <div className="summary-row"><span>{bus.layout === "sleeper" ? "Berth" : "Seat"}</span><b>{selected}</b></div>
      <div className="summary-row"><span>Base fare</span><b>₹{bus.fare.toLocaleString("en-IN")}</b></div>
      <div className="summary-total"><span>Total price</span><strong>₹{bus.fare.toLocaleString("en-IN")}</strong></div>
    </aside>
  );
}

function BookingDetails({ bus, source, destination, date, selected, boarding, dropping, setBoarding, setDropping, onBack, onContinue }: {
  bus: Bus; source: string; destination: string; date: string; selected: string; boarding: string; dropping: string; setBoarding: (v: string) => void; setDropping: (v: string) => void; onBack: () => void; onContinue: () => void;
}) {
  return (
    <div className="page-wrap narrow">
      <PageTop label="BOOKING DETAILS" title="Almost there" subtitle="Add passenger and stop details to continue." onBack={onBack} />
      <div className="details-grid">
        <div className="form-stack">
          <section className="form-card"><div className="section-number">1</div><div className="form-content"><h2>Passenger details</h2><p>We'll send the ticket to these contact details.</p><div className="input-grid"><label>Full name<input defaultValue="Arjun Kumar" /></label><label>Age<input defaultValue="29" type="number" /></label><label>Gender<select defaultValue="Male"><option>Male</option><option>Female</option><option>Other</option></select></label><label>Mobile number<input defaultValue="+91 98765 43210" /></label><label className="wide">Email address<input defaultValue="arjun.kumar@example.com" type="email" /></label></div></div></section>
          <section className="form-card"><div className="section-number">2</div><div className="form-content"><h2>Pick-up & drop-off</h2><p>Select the most convenient stops for your journey.</p><label className="select-stop"><span><i className="dot source-dot" /><b>BOARDING STOP</b></span><select value={boarding} onChange={(e) => setBoarding(e.target.value)}><option>Majestic Bus Station — 21:00</option><option>Indiranagar — 21:20</option><option>Hebbal Flyover — 21:45</option></select></label><label className="select-stop"><span><i className="dot destination-dot" /><b>DROPPING STOP</b></span><select value={dropping} onChange={(e) => setDropping(e.target.value)}><option>MGBS, Hyderabad — 06:15</option><option>Mehdipatnam — 05:50</option><option>Lakdikapul — 06:05</option></select></label></div></section>
        </div>
        <div><TripSummary bus={bus} source={source} destination={destination} date={date} selected={selected} /><Button onClick={onContinue} className="full-button continue-button">Continue to payment <Icon name="arrow" /></Button></div>
      </div>
    </div>
  );
}

function Payment({ bus, selected, method, setMethod, onBack, onPay }: { bus: Bus; selected: string; method: string; setMethod: (v: string) => void; onBack: () => void; onPay: () => void }) {
  const methods = [{ id: "upi", label: "UPI", sub: "Google Pay, PhonePe, BHIM", icon: "wallet" }, { id: "card", label: "Card", sub: "Credit or debit card", icon: "card" }, { id: "net", label: "Net Banking", sub: "All major Indian banks", icon: "shield" }];
  return (
    <div className="page-wrap payment-wrap">
      <PageTop label="SECURE PAYMENT" title="Complete your payment" subtitle="Your seat is held for 09:42 minutes." onBack={onBack} />
      <div className="payment-grid">
        <section className="payment-card">
          <h2>Choose payment method</h2>
          <div className="payment-methods">{methods.map((item) => <button key={item.id} className={method === item.id ? "active" : ""} onClick={() => setMethod(item.id)}><span><Icon name={item.icon} /></span><div><b>{item.label}</b><small>{item.sub}</small></div><i>{method === item.id && <em />}</i></button>)}</div>
          <div className="payment-entry">
            {method === "upi" && <><label>UPI ID<input placeholder="name@bank" defaultValue="arjun@okaxis" /></label><p>Open your UPI app and approve the payment request.</p></>}
            {method === "card" && <><label>Card number<input placeholder="0000 0000 0000 0000" /></label><div className="two-inputs"><label>Expiry<input placeholder="MM / YY" /></label><label>CVV<input placeholder="•••" /></label></div></>}
            {method === "net" && <label>Select your bank<select><option>HDFC Bank</option><option>State Bank of India</option><option>ICICI Bank</option><option>Axis Bank</option></select></label>}
          </div>
        </section>
        <aside className="pay-summary"><span className="summary-icon"><Icon name="shield" /></span><h3>Payment summary</h3><div className="summary-row"><span>{bus.name}</span><b>{selected}</b></div><div className="summary-row"><span>Ticket fare</span><b>₹{bus.fare.toLocaleString("en-IN")}</b></div><div className="summary-row"><span>Booking fee</span><b>₹0</b></div><div className="summary-total"><span>Amount to pay</span><strong>₹{bus.fare.toLocaleString("en-IN")}</strong></div><Button onClick={onPay} className="full-button">Pay ₹{bus.fare.toLocaleString("en-IN")} securely</Button><small className="center-note"><Icon name="shield" size={14} /> 256-bit encrypted payment</small></aside>
      </div>
    </div>
  );
}

function QRCode() {
  const pattern = "111111100101011111111000001010111010000011011101001101011011101101110100010101011101101110101110101011101100000101000101000001111111101010101111111000000000110100000000101111101101110100101100100011001011100110101011100101101101010101110101011001010001010101101100100111101000011011101100101011101010000010000001010001111111101010101101101000001011101100100011011101001010111001111011011101101100100000011000001001011111111101011110110101";
  return <div className="qr" aria-label="Booking QR code">{pattern.split("").map((bit, i) => <i key={i} className={bit === "1" ? "dark" : ""} />)}</div>;
}

function Confirmed({ bus, source, destination, date, selected, onTicket, onHome }: { bus: Bus; source: string; destination: string; date: string; selected: string; onTicket: () => void; onHome: () => void }) {
  return (
    <div className="confirmation-page">
      <div className="success-mark"><Icon name="check" size={34} /></div>
      <span className="eyebrow">PAYMENT SUCCESSFUL</span><h1>Booking confirmed</h1><p>Your journey is all set. A copy of your ticket has been sent to your email.</p>
      <article className="confirmation-ticket">
        <div className="ticket-route"><div><small>FROM</small><b>{source}</b><span>{bus.departure}</span></div><div className="ticket-bus"><Icon name="bus" /><i /></div><div><small>TO</small><b>{destination}</b><span>{bus.arrival}</span></div></div>
        <div className="ticket-details"><div><small>TRAVEL DATE</small><b>{date}</b></div><div><small>BUS</small><b>{bus.name}</b></div><div><small>SEAT / BERTH</small><b className="seat-pill">{selected}</b></div><div><small>BOOKING ID</small><b>VR8K42P9</b></div></div>
        <div className="ticket-qr"><QRCode /><div><b>Scan to verify</b><small>Show this QR code while boarding</small></div></div>
      </article>
      <div className="confirmation-actions"><Button onClick={onTicket}><Icon name="ticket" /> View digital ticket</Button><Button variant="secondary" onClick={onHome}>Back to dashboard</Button></div>
    </div>
  );
}

function DigitalTicket({ bus, source, destination, date, selected, boarding, dropping, onHome }: { bus: Bus; source: string; destination: string; date: string; selected: string; boarding: string; dropping: string; onHome: () => void }) {
  return (
    <div className="page-wrap ticket-page">
      <PageTop label="DIGITAL TICKET" title="Ready to board" subtitle="Keep this ticket handy for a smooth boarding experience." />
      <article className="digital-ticket">
        <div className="digital-ticket-head"><div className="footer-brand"><span className="brand-mark"><Icon name="bus" size={18} /></span><b>ViaRoute</b></div><span>CONFIRMED</span></div>
        <div className="digital-route"><div><small>FROM</small><b>{source}</b><strong>{bus.departure}</strong></div><div><Icon name="bus" /><span>{bus.duration}</span></div><div><small>TO</small><b>{destination}</b><strong>{bus.arrival}</strong></div></div>
        <div className="digital-info"><div><small>PASSENGER</small><b>Arjun Kumar</b></div><div><small>DATE</small><b>{date}</b></div><div><small>BUS</small><b>{bus.name}</b></div><div><small>SEAT / BERTH</small><b>{selected}</b></div><div><small>BOARDING</small><b>{boarding.split(" — ")[0]}</b></div><div><small>DROPPING</small><b>{dropping.split(" — ")[0]}</b></div></div>
        <div className="digital-bottom"><div><small>BOOKING ID</small><b>VR8K42P9</b><span>Paid · ₹{bus.fare.toLocaleString("en-IN")}</span></div><QRCode /></div>
      </article>
      <div className="confirmation-actions"><Button onClick={() => window.print()}><Icon name="download" /> Download ticket</Button><Button variant="secondary" onClick={onHome}>Back to dashboard</Button></div>
    </div>
  );
}

function MyBookings({ onTicket, onTrack }: { onTicket: () => void; onTrack: () => void }) {
  const [activeTab, setActiveTab] = useState<"upcoming" | "completed" | "cancelled">("upcoming");
  const [tripCancelled, setTripCancelled] = useState(false);
  const [showCancel, setShowCancel] = useState(false);
  const [messageTarget, setMessageTarget] = useState<"driver" | "agency" | null>(null);
  const [message, setMessage] = useState("");
  const [messageSent, setMessageSent] = useState(false);

  const sendMessage = () => {
    if (!message.trim()) return;
    setMessageSent(true);
    setMessage("");
  };

  const confirmCancellation = () => {
    setTripCancelled(true);
    setShowCancel(false);
    setActiveTab("cancelled");
  };

  return (
    <div className="page-wrap">
      <PageTop label="YOUR JOURNEYS" title="My bookings" subtitle="Manage tickets and keep track of upcoming trips." />
      <div className="booking-tabs">
        <button className={activeTab === "upcoming" ? "active" : ""} onClick={() => setActiveTab("upcoming")}>Upcoming <span>{tripCancelled ? 0 : 1}</span></button>
        <button className={activeTab === "completed" ? "active" : ""} onClick={() => setActiveTab("completed")}>Completed <span>2</span></button>
        <button className={activeTab === "cancelled" ? "active" : ""} onClick={() => setActiveTab("cancelled")}>Cancelled <span>{tripCancelled ? 1 : 0}</span></button>
      </div>

      {activeTab === "upcoming" && !tripCancelled && (
        <article className="booking-card">
          <div className="booking-date"><b>22</b><span>OCT</span><small>2026</small></div>
          <div className="booking-body"><div className="booking-status"><span>UPCOMING</span><small>Booking ID: VR8K42P9</small></div><h2>Bengaluru <Icon name="arrow" /> Hyderabad</h2><p>GreenLine Night Rider · A/C Sleeper</p><div className="booking-meta"><span><Icon name="clock" /> 21:30 — 06:15</span><span><Icon name="seat" /> Berth L04</span><span><Icon name="pin" /> Majestic Bus Station</span></div></div>
          <div className="booking-actions">
            <Button onClick={onTrack}>Track bus</Button>
            <Button variant="secondary" onClick={onTicket}>View ticket</Button>
            <button className="booking-link" onClick={() => { setMessageTarget("driver"); setMessageSent(false); }}>Message driver</button>
            <button className="booking-link" onClick={() => { setMessageTarget("agency"); setMessageSent(false); }}>Message agency</button>
            <button className="booking-link danger" onClick={() => setShowCancel(true)}>Cancel ticket</button>
          </div>
        </article>
      )}

      {activeTab === "upcoming" && tripCancelled && (
        <BookingEmpty title="No upcoming trips" copy="When you book your next journey, it will appear here." action="Search buses" />
      )}

      {activeTab === "completed" && (
        <div className="booking-list">
          <PastBooking date="12" month="JUL" route="Chennai → Bengaluru" bus="KSRTC Airavat Club Class" seat="Seat 8A" amount="₹1,175" onTicket={onTicket} />
          <PastBooking date="03" month="MAR" route="Pune → Mumbai" bus="IntrCity SmartBus" seat="Seat 4D" amount="₹649" onTicket={onTicket} />
        </div>
      )}

      {activeTab === "cancelled" && (
        tripCancelled ? (
          <article className="booking-card cancelled-booking">
            <div className="booking-date"><b>22</b><span>OCT</span><small>2026</small></div>
            <div className="booking-body"><div className="booking-status cancelled"><span>CANCELLED</span><small>Booking ID: VR8K42P9</small></div><h2>Bengaluru <Icon name="arrow" /> Hyderabad</h2><p>GreenLine Night Rider · Refund initiated</p><div className="booking-meta"><span><Icon name="clock" /> Cancelled just now</span><span><Icon name="wallet" /> ₹1,169 refund</span><span><Icon name="shield" /> Expected in 3–5 days</span></div></div>
            <div className="booking-actions"><Button variant="secondary" onClick={() => { setMessageTarget("agency"); setMessageSent(false); }}>Message agency</Button></div>
          </article>
        ) : <BookingEmpty title="No cancelled trips" copy="Bookings you cancel will appear here with their refund status." />
      )}

      {showCancel && (
        <div className="modal-backdrop" role="presentation" onClick={() => setShowCancel(false)}>
          <div className="action-modal" role="dialog" aria-modal="true" aria-labelledby="cancel-title" onClick={(e) => e.stopPropagation()}>
            <span className="modal-icon danger"><Icon name="ticket" /></span>
            <h2 id="cancel-title">Cancel this ticket?</h2>
            <p>Your berth L04 will be released. A cancellation fee of ₹130 applies.</p>
            <div className="refund-box"><span>Ticket amount<b>₹1,299</b></span><span>Cancellation fee<b>− ₹130</b></span><span><strong>Refund amount</strong><strong>₹1,169</strong></span></div>
            <div className="modal-actions"><Button variant="secondary" onClick={() => setShowCancel(false)}>Keep booking</Button><button className="danger-button" onClick={confirmCancellation}>Cancel ticket</button></div>
          </div>
        </div>
      )}

      {messageTarget && (
        <div className="modal-backdrop" role="presentation" onClick={() => setMessageTarget(null)}>
          <div className="action-modal message-modal" role="dialog" aria-modal="true" aria-labelledby="message-title" onClick={(e) => e.stopPropagation()}>
            <span className="modal-icon"><Icon name={messageTarget === "driver" ? "user" : "bus"} /></span>
            <h2 id="message-title">Message {messageTarget === "driver" ? "your driver" : "GreenLine agency"}</h2>
            <p>{messageTarget === "driver" ? "Ravi Shankar usually replies within a few minutes while the bus is stationary." : "Ask the operator about boarding, luggage, amenities, or your booking."}</p>
            {messageSent ? (
              <div className="message-success"><Icon name="check" /><div><b>Message sent</b><span>We'll notify you when they reply.</span></div></div>
            ) : (
              <>
                <div className="quick-messages">
                  {["Where is the boarding point?", "Is the bus on time?", "I need help with luggage"].map((item) => <button key={item} onClick={() => setMessage(item)}>{item}</button>)}
                </div>
                <label className="message-field">Your message<textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type your message..." /></label>
              </>
            )}
            <div className="modal-actions"><Button variant="secondary" onClick={() => setMessageTarget(null)}>{messageSent ? "Close" : "Cancel"}</Button>{!messageSent && <Button disabled={!message.trim()} onClick={sendMessage}>Send message</Button>}</div>
          </div>
        </div>
      )}
    </div>
  );
}

function PastBooking({ date, month, route, bus, seat, amount, onTicket }: { date: string; month: string; route: string; bus: string; seat: string; amount: string; onTicket: () => void }) {
  return (
    <article className="booking-card">
      <div className="booking-date completed"><b>{date}</b><span>{month}</span><small>2025</small></div>
      <div className="booking-body"><div className="booking-status completed"><span>COMPLETED</span><small>Paid · {amount}</small></div><h2>{route}</h2><p>{bus}</p><div className="booking-meta"><span><Icon name="check" /> Journey completed</span><span><Icon name="seat" /> {seat}</span><span><Icon name="ticket" /> Ticket verified</span></div></div>
      <div className="booking-actions"><Button variant="secondary" onClick={onTicket}>View ticket</Button><button className="booking-link">Rate journey</button></div>
    </article>
  );
}

function BookingEmpty({ title, copy, action }: { title: string; copy: string; action?: string }) {
  return (
    <div className="booking-empty">
      <span><Icon name="ticket" size={28} /></span>
      <h2>{title}</h2>
      <p>{copy}</p>
      {action && <Button onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}>{action}</Button>}
    </div>
  );
}

function TrackBus({ source, destination, onBack }: { source: string; destination: string; onBack: () => void }) {
  return (
    <div className="page-wrap">
      <PageTop label="LIVE TRACKING" title="Your bus is on the way" subtitle="Location updated just now." onBack={onBack} />
      <div className="track-grid">
        <section className="map-card">
          <div className="map-pattern" />
          <div className="map-road road-one" /><div className="map-road road-two" /><div className="map-road road-three" />
          <div className="map-label label-one">Yelahanka</div><div className="map-label label-two">Chikkaballapur</div><div className="map-label label-three">Bagepalli</div>
          <div className="map-start"><i />{source}</div><div className="map-bus"><Icon name="bus" /><span>GreenLine</span></div><div className="map-end"><i />{destination}</div>
        </section>
        <aside className="tracking-panel">
          <span className="live-badge"><i /> LIVE</span><h2>GreenLine Night Rider</h2><p>A/C Sleeper · KA 01 AB 4582</p>
          <div className="eta-card"><small>ESTIMATED ARRIVAL</small><b>06:10 AM</b><span>5 min early</span></div>
          <div className="track-timeline"><div className="done"><i><Icon name="check" size={13} /></i><span><b>Departed {source}</b><small>21:30 · On time</small></span></div><div className="current"><i><Icon name="bus" size={15} /></i><span><b>Near Chikkaballapur</b><small>Current location · 22:38</small></span></div><div><i /><span><b>Anantapur</b><small>Estimated 01:15</small></span></div><div><i /><span><b>Arrive {destination}</b><small>Estimated 06:10</small></span></div></div>
          <div className="driver-card"><span>RS</span><div><small>YOUR DRIVER</small><b>Ravi Shankar</b><em>4.9 rating</em></div><Button variant="secondary">Call driver</Button></div>
        </aside>
      </div>
    </div>
  );
}

export default App;

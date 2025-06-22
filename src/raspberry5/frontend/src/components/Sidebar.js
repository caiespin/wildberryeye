function Sidebar({ onSelect, selected }) {
  const sections = ["Home", "About", "Contact"];

  return (
    <nav className="sidebar">
      <ul>
        {sections.map((section) => (
          <li
            key={section}
            className={selected === section ? "active" : ""}
            onClick={() => onSelect(section)}
          >
            {section}
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Sidebar;

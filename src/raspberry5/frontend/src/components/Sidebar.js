function Sidebar({ onSelect, selected }) {
  const sections = ["Bee's Video", "Bird's Video", "Data Analytics"];

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

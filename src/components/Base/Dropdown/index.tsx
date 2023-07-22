import React, { useState } from "react";
import Icon from "@mdi/react";
import { mdiMenuDown } from "@mdi/js";

import "./BaseDropdown.scss";

interface DropdownMenuProps {
  options: string[];
}

const DropdownMenu: React.FC<DropdownMenuProps> = ({ options }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="dropdown">
      <div className="dropdown-toggle" onClick={toggleDropdown}>
        English
        <Icon path={mdiMenuDown} size={0.8} />
      </div>
      {isOpen && (
        <ul className="dropdown-menu">
          {options.map((option, index) => (
            <li key={index}>{option}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropdownMenu;

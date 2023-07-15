import { ReactNode } from "react";

import { useLocation, useNavigate } from "react-router-dom";

import { routers } from "../routers";
import "./DefaultLayout.scss";

export interface BaseLayoutProps {
  children: ReactNode;
}

function DefaultLayout({ children }: BaseLayoutProps) {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div id="default-layout">
      <header className="siderbar">
        <img src="/images/sidebar_logo.svg" alt="logo" />
        <div className="devider my-6"></div>
        <ul className="menu">
          {routers.map((item) => {
            if (item.isShowSideBar)
              return (
                <li
                  key={item.name}
                  className={`menu__item ${
                    item.path === location.pathname ? "active" : ""
                  }`}
                  onClick={() => navigate(item.path!)}
                >
                  {item.icon}
                  {item.name}
                </li>
              );
          })}
        </ul>
      </header>
      <main>{children}</main>
    </div>
  );
}

export default DefaultLayout;

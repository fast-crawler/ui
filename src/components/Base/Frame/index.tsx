import { ReactNode } from "react";
import Icon from "@mdi/react";
import { mdiGithub } from "@mdi/js";

import "./BaseFrame.scss";
import DropdownMenu from "../Dropdown";

export interface BaseFrameProps {
  title: string;
  children: ReactNode;
}

function BaseFrame({ title, children }: BaseFrameProps) {
  return (
    <div className="base-frame">
      <div className="header">
        <h2>{title}</h2>
        <div className="header__lang">
          <Icon
            path={mdiGithub}
            size={1.34}
            color="var(--color-text)"
            className="mr-2"
          />
          <DropdownMenu options={["English"]} />
        </div>
      </div>
      <div className="container">{children}</div>
    </div>
  );
}

export default BaseFrame;

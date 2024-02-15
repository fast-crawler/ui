import { ReactNode, useState } from "react";
import Icon from "@mdi/react";
import { mdiGithub, mdiArrowLeft } from "@mdi/js";
import { useNavigate } from "react-router-dom";

import "./BaseFrame.scss";
import DropdownMenu from "../Dropdown";

export interface BaseFrameProps {
  title: string;
  isBack?: boolean;
  children: ReactNode;
}

function BaseFrame({ title, isBack = false, children }: BaseFrameProps) {
  const [lang, setLang] = useState<string>("English");
  const navigate = useNavigate();

  return (
    <div className="base-frame">
      <div className="header flex-none">
        <h2 className="text-2xl font-bold">{title}</h2>
        {isBack ? (
          <button
            className="btn-primary text-text bg-bg-text flex items-center gap-2 pl-3"
            onClick={() => navigate(-1)}
          >
            <Icon path={mdiArrowLeft} size={0.8} />
            back
          </button>
        ) : (
          <div className="header__lang">
            <Icon
              path={mdiGithub}
              size={1.34}
              color="var(--color-text)"
              className="mr-2"
            />
            <DropdownMenu title={lang} setTitle={setLang} items={["English"]} />
          </div>
        )}
      </div>
      <div className="divider mb-6"></div>
      <div className="contain">{children}</div>
    </div>
  );
}

export default BaseFrame;

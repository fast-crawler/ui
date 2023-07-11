import { Routes, Route } from "react-router-dom";

import { routers } from "./routers";

function App() {
  return (
    <div id="App">
      <Routes>
        {routers.map((router, index) => {
          if (!router.hasChild)
            return (
              <Route key={index} path={router.path} element={router.element} />
            );
          return router.children?.map((child) => (
            <Route key={child.name} path={child.path} element={child.element} />
          ));
        })}
      </Routes>
    </div>
  );
}

export default App;

import { Routes, Route } from "react-router-dom";

import { routers } from "./routers";
import DefaultLayout from "./layouts/DefaultLayout";

function App() {
  return (
    <div id="App">
      <DefaultLayout>
        <Routes>
          {routers.map((router, index) => {
            if (!router.hasChild)
              return (
                <Route
                  key={index}
                  path={router.path}
                  element={router.element}
                />
              );
            return router.children?.map((child) => (
              <Route
                key={child.name}
                path={child.path}
                element={child.element}
              />
            ));
          })}
        </Routes>
      </DefaultLayout>
    </div>
  );
}

export default App;

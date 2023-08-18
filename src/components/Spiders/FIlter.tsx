import { Menu, Transition } from "@headlessui/react";
import { Fragment } from "react";
import { Icon } from "@mdi/react";
import { mdiMenuDown, mdiFilter } from "@mdi/js";

export interface SpidersFilterProps {
  selectedSort: number;
  onSortChange: (newValue: number) => void;
  selectedState: number;
  onStateChange: (newValue: number) => void;
}

function SpidersFilter({
  selectedSort,
  selectedState,
  onSortChange,
  onStateChange,
}: SpidersFilterProps) {
  const sortOptions = [
    { label: "Name", value: 1 },
    { label: "State", value: 2 },
    { label: "Started at", value: 3 },
    { label: "Duration", value: 4 },
  ];

  const stateOptions = [
    { label: "All", value: 1 },
    { label: "Active", value: 2 },
    { label: "Paused", value: 3 },
    { label: "Finished", value: 4 },
  ];

  return (
    <Menu as="div" className="relative inline-block text-left z-30">
      {({ open }) => (
        <>
          <div className="transition-all duration-300">
            <Menu.Button className="bg-white border border-border text-text px-2 py-2 rounded-lg font-semibold flex items-center">
              <Icon path={mdiFilter} size={0.8} className="mr-2" />
              Filter
              <Icon
                className={`ml-2 ${open ? "rotate-180" : ""}`}
                path={mdiMenuDown}
                size={1}
              />
            </Menu.Button>
          </div>
          <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items className="absolute left-0 mt-2 w-56 origin-top-left divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <div className="p-5" style={{ fontFamily: "Inter" }}>
                <h4 className="text-primary text-sm font-medium mb-2">
                  SORT BY :{" "}
                </h4>
                {sortOptions.map((option) => (
                  <label
                    key={option.value}
                    className="flex items-center justify-between cursor-pointer hover:bg-bg-primary p-1 px-2 rounded-md"
                  >
                    <span className="text-gray-800 text-sm">
                      {option.label}
                    </span>
                    <input
                      type="radio"
                      value={1}
                      checked={selectedSort === option.value}
                      onChange={() => onSortChange(option.value)}
                      className="form-radio h-4 w-4 text-primary"
                    />
                  </label>
                ))}
                <div className="h-[2px] bg-border my-3"></div>
                <h4 className="text-primary text-sm font-medium mb-2">
                  STATE :{" "}
                </h4>
                {stateOptions.map((option) => (
                  <label
                    key={option.value}
                    className="flex items-center justify-between cursor-pointer hover:bg-bg-primary p-1 px-2 rounded-md"
                  >
                    <span className="text-gray-800 text-sm">
                      {option.label}
                    </span>
                    <input
                      type="radio"
                      value={1}
                      checked={selectedState === option.value}
                      onChange={() => onStateChange(option.value)}
                      className="form-radio h-4 w-4 text-primary"
                    />
                  </label>
                ))}
              </div>
            </Menu.Items>
          </Transition>
        </>
      )}
    </Menu>
  );
}

export default SpidersFilter;

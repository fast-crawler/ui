import { Menu, Transition } from "@headlessui/react";
import { Fragment } from "react";
import { Icon } from "@mdi/react";
import { mdiMenuDown } from "@mdi/js";

export interface BaseDropdownProps {
  title: string;
  items: string[];
  setTitle: (newValue: string) => void;
}

function BaseDropdown({ title, items, setTitle }: BaseDropdownProps) {
  return (
    <Menu as="div" className="relative inline-block text-left">
      {({ open }) => (
        <>
          <div className="transition-all duration-300">
            <Menu.Button className="bg-bg-text px-4 py-2 rounded-lg font-semibold flex">
              {title}
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
            <Menu.Items className="absolute right-0 mt-2 w-32 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
              <div className="p-2">
                {items.map((item) => (
                  <Menu.Item key={item}>
                    {({ active }) => (
                      <button
                        className={`${
                          active || item === title
                            ? "bg-bg-primary text-primary"
                            : "text-black"
                        } group flex w-full items-center rounded-md px-2 py-2 mb-1 text-sm`}
                        onClick={() => setTitle(item)}
                      >
                        {item}
                      </button>
                    )}
                  </Menu.Item>
                ))}
              </div>
            </Menu.Items>
          </Transition>
        </>
      )}
    </Menu>
  );
}

export default BaseDropdown;

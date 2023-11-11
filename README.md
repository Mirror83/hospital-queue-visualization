# Hospital queue visualization
A visualization of the operations of an adaptable priority queue. It is made with [pygame](https://www.pygame.org/)

## Status
**In progress**

Basic building blocks are in place:
1. The adaptable priority queue implementation is present and error-free (take the error-free part lightly; it is not
thoroughly tested)
2. A basic graphics set up is present

### Remaining Tasks
This is a high-level description of what is yet to be done.
- [x] Draw the hospital
- [x] Draw patients as graphics, not rectangles
- [x] Manage dialogs from within pygame instead of from Tkinter. The previous approach made the OS think
the app is unresponsive if the Tkinter dialog was not dismissed promptly.
- [ ] Polish the entry controls
- [ ] **Additional** - Animate the patients to walk as they get into the queue at their correct positions.
This animation should also be run after a priority change.
- [ ] **Additional** - Improve overall aesthetics
- **Important, but additional** Make `TextButton`s and `TextInput`s listen for input and events independent of the
- event loop in main.py

> [!NOTE]
> When a dialog pops up, the other items are still focusable; but the `TextButton`s do nothing when pressed but
> input is still recorded by the `TextInput`s. This is something that I may or may not resolve, since it is quite
> discouraging to have to create UI elements (in pygame) when other frameworks handle it quite easily.
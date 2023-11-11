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
- [ ] Draw the hospital
- [ ] Draw patients as graphics, not rectangles
- [ ] Polish the entry controls 
- [x] Manage dialogs from within pygame instead of from Tkinter. The current approach makes the OS think 
the app is unresponsive if the Tkinter dialog is not dismissed promptly.
- [ ] **Additional** - Animate the patients to walk as they get into the queue at their correct positions.
This animation should also be run after a priority change.

> [!NOTE]
> When a dialog pops up, the other items are still focusable; but the `TextButtons` do nothing when pressed but
> input is still recorded by the `TextInputs`. This is something that I may or may not resolve, since it is quite
> discouraging to have to create UI elements (in pygame) when other frameworks handle it quite easily.
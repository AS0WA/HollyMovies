document.getElementById('context-menu').addEventListener('contextmenu', function(event) {
  event.preventDefault(); // Prevent default browser context menu

  // Calculate appropriate position for context menu
  const menuX = event.clientX;
  const menuY = event.clientY;

  // Show the context menu at calculated position
  const contextMenu = document.getElementById('context-menu');
  contextMenu.style.left = menuX + 'px';
  contextMenu.style.top = menuY + 'px';
  contextMenu.classList.remove('hidden');

  // Add click event listener to each menu item
  contextMenu.querySelectorAll('li a').forEach(item => {
    item.addEventListener('click', function(event) {
      event.preventDefault();

      // Perform action based on data-action attribute
      const action = this.dataset.action;
      // Handle action logic here (e.g., execute function, trigger event)

      // Hide context menu after action is performed
      contextMenu.classList.add('hidden');
    });
  });
});

// Optionally, add a click event listener outside the context menu to hide it
document.addEventListener('click', function(event) {
  const contextMenu = document.getElementById('context-menu');
  if (!contextMenu.contains(event.target)) {
    contextMenu.classList.add('hidden');
  }
});
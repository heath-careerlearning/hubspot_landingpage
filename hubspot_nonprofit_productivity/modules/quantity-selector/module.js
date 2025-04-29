window.addEventListener('load', function() {
  const wrapper = document.querySelector('.quantity-selector-wrapper');
  if (!wrapper) return;

  const quantityInput = wrapper.querySelector('.quantity-input');
  const decreaseBtn = wrapper.querySelector('.qty-btn.decrease');
  const increaseBtn = wrapper.querySelector('.qty-btn.increase');
  const amountDisplay = wrapper.querySelector('.amount');
  const basePrice = parseFloat(amountDisplay.dataset.basePrice);

  function updatePrice() {
    const quantity = parseInt(quantityInput.value) || 1;
    const totalPrice = (basePrice * quantity).toFixed(2);
    amountDisplay.textContent = totalPrice;
  }

  function handleQuantityChange(change) {
    const currentValue = parseInt(quantityInput.value) || 1;
    const newValue = currentValue + change;
    const min = parseInt(quantityInput.min) || 1;
    const max = parseInt(quantityInput.max) || 99;

    if (newValue >= min && newValue <= max) {
      quantityInput.value = newValue;
      updatePrice();
    }
  }

  decreaseBtn.addEventListener('click', () => handleQuantityChange(-1));
  increaseBtn.addEventListener('click', () => handleQuantityChange(1));
  
  quantityInput.addEventListener('change', () => {
    const value = parseInt(quantityInput.value) || 1;
    const min = parseInt(quantityInput.min) || 1;
    const max = parseInt(quantityInput.max) || 99;
    
    quantityInput.value = Math.min(Math.max(value, min), max);
    updatePrice();
  });
}); 
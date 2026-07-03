export function calculateOrderTotal(items) {
    const total = items.reduce((sum, item) => {
        return sum + item.price * item.quantity;
    }, 0);

    return total;
}

//nolur şu commiti gör

export function applyDiscount(total, discountRate) {
    const discountAmount = total * discountRate;
    const finalTotal = total - discountAmount;

    return finalTotal;
}
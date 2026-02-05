/**
 * Deal Analyzer
 * By HAL 9000
 * 
 * Analyze a potential deal for resale viability.
 */

function analyzeDeal(deal) {
  const {
    name,
    originalPrice,
    dealPrice,
    estimatedResalePrice,
    category,
    weight = 0.5, // kg
    effort = 'medium' // low, medium, high
  } = deal;
  
  const discount = ((originalPrice - dealPrice) / originalPrice) * 100;
  const margin = estimatedResalePrice - dealPrice;
  const marginPercent = (margin / dealPrice) * 100;
  const roi = (margin / dealPrice) * 100;
  
  // Shipping estimate (Portugal)
  const shippingCost = weight < 0.5 ? 3 : weight < 2 ? 5 : 8;
  const netMargin = margin - shippingCost;
  
  const score = calculateScore({
    discount,
    netMargin,
    effort,
    category
  });
  
  return {
    name,
    investment: dealPrice,
    discount: `${discount.toFixed(1)}%`,
    grossMargin: `€${margin.toFixed(2)}`,
    netMargin: `€${netMargin.toFixed(2)}`,
    roi: `${roi.toFixed(1)}%`,
    score,
    verdict: score >= 70 ? '✅ BUY' : score >= 50 ? '🤔 MAYBE' : '❌ SKIP'
  };
}

function calculateScore({ discount, netMargin, effort, category }) {
  let score = 0;
  
  // Discount (max 30 points)
  score += Math.min(discount * 0.5, 30);
  
  // Net margin (max 40 points)
  score += Math.min(netMargin * 2, 40);
  
  // Effort (max 15 points)
  const effortScores = { low: 15, medium: 10, high: 5 };
  score += effortScores[effort] || 10;
  
  // Category bonus (max 15 points)
  const categoryBonus = {
    perfume: 15,
    sneakers: 12,
    lego: 12,
    electronics: 8,
    clothing: 10,
    other: 5
  };
  score += categoryBonus[category] || 5;
  
  return Math.round(score);
}

// Example usage
const exampleDeal = {
  name: 'Nike Air Max 90',
  originalPrice: 150,
  dealPrice: 45,
  estimatedResalePrice: 90,
  category: 'sneakers',
  weight: 0.8,
  effort: 'low'
};

console.log('Deal Analysis:');
console.log(analyzeDeal(exampleDeal));

module.exports = { analyzeDeal };

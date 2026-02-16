import json
import random

class EcoBot:
    def __init__(self):
        # Load mock data
        with open('data/products.json', 'r') as f:
            self.products = json.load(f)
        with open('data/orders.json', 'r') as f:
            self.orders = json.load(f)
        
        # User session state (In a real app, use a database or Redis)
        self.user_sessions = {}

    def get_session(self, user_id):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {'eco_mode': False}
        return self.user_sessions[user_id]

    def toggle_eco_mode(self, user_id):
        session = self.get_session(user_id)
        session['eco_mode'] = not session['eco_mode']
        state = "ON" if session['eco_mode'] else "OFF"
        return f"🌿 Sustainability Mode is now **{state}**. I will {'' if session['eco_mode'] else 'not'} prioritize eco-friendly products."

    def search_products(self, user_id, query):
        session = self.get_session(user_id)
        results = []
        
        for p in self.products:
            # Simple keyword matching
            if query.lower() in p['name'].lower() or query.lower() in p['category'].lower():
                # If Eco Mode is ON, only show eco-friendly items
                if session['eco_mode'] and not p['eco_friendly']:
                    continue
                results.append(p)
        
        if not results:
            if session['eco_mode']:
                return "I couldn't find any eco-friendly products matching that. Try turning off Eco Mode to see more results."
            return "No products found."

        response = "Here is what I found:\n"
        for p in results:
            icon = "🌱" if p['eco_friendly'] else ""
            response += f"- {icon} **{p['name']}** (${p['price']}) - {p['description']}\n"
        return response

    def track_order(self, order_id):
        order = self.orders.get(order_id.upper())
        if order:
            return f"📦 **Order {order_id}**: Status is **{order['status']}**. Items: {', '.join(order['items'])}."
        return "I couldn't find that order ID. Please check and try again (e.g., ORD-999)."

    def process_message(self, user_id, message):
        msg = message.lower()
        
        # Intent: Toggle Eco Mode
        if "eco mode" in msg or "sustainability" in msg:
            return self.toggle_eco_mode(user_id)
        
        # Intent: Track Order
        if "track" in msg or "order" in msg:
            # Extract potential Order ID (simple logic)
            words = message.split()
            for word in words:
                if word.upper().startswith("ORD-"):
                    return self.track_order(word)
            return "Please provide your Order ID (starts with ORD-)."

        # Intent: Product Search (Catch-all)
        return self.search_products(user_id, message)

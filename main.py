# Data #

recipes = {
    "small": {
        "ingredients": {
            "bread": 2,  # slice
            "ham": 4,  # slice
            "cheese": 4,  # ounces
        },
        "cost": 1.75,
    },
    "medium": {
        "ingredients": {
            "bread": 4,  # slice
            "ham": 6,  # slice
            "cheese": 8,  # ounces
        },
        "cost": 3.25,
    },
    "large": {
        "ingredients": {
            "bread": 6,  # slice
            "ham": 8,  # slice
            "cheese": 12,  # ounces
        },
        "cost": 5.5,
    }
}

original_resources = {
    "bread": 12,  # slice
    "ham": 18,  # slice
    "cheese": 24,  # ounces
}

resources = original_resources.copy()


# Complete functions #

class SandwichMachine:

    def __init__(self, machine_resources, original_resources):
        """Receives resources as input.
           Hint: bind input variable to self variable"""
        self.machine_resources = machine_resources
        self.original_resources = original_resources
        self.total_sandwiches_sold = 0
        self.total_revenue = 0.0
        self.resupply_count = 0
        self.ingredient_usage = {key: 0 for key in machine_resources.keys()}
        self.transaction_history = []
        self.revenue_breakdown = {"small": 0.0, "medium": 0.0, "large": 0.0}
        self.customer_orders = {i: [] for i in range(1, 11)}


    def check_resources(self, ingredients):
        """Returns True when order can be made, False if ingredients are insufficient."""
        for item in ingredients:
            if ingredients[item] > self.machine_resources[item]:
                return False, item
            return True, None

    def process_coins(self):
        """Returns the total calculated from coins inserted.
           Hint: include input() function here, e.g. input("how many quarters?: ")"""
        print("Please insert money -> ")
        total = float(input("How much will you put in? "))
        return total

    def transaction_result(self, coins, cost):
        """Return True when the payment is accepted, or False if money is insufficient.
           Hint: use the output of process_coins() function for cost input"""
        if coins >= cost:
            change = round(coins - cost, 2)
            if change > 0:
                print(f"Here is ${change:.2f} in change ")
                self.total_revenue += cost
                return True
            else:
                print("Sorry the money you put in is insufficient. It is now being returned. ")
                return False

    def make_sandwich(self, sandwich_size, order_ingredients, customer_id, quantity):
        """Deduct the required ingredients from the resources.
           Hint: no output"""
        for item in order_ingredients:
            self.machine_resources[item] -= order_ingredients[item] * quantity
            self.ingredient_usage[item] += order_ingredients[item] * quantity
        self.total_sandwiches_sold += quantity
        self.revenue_breakdown[sandwich_size] += recipes[sandwich_size]["cost"] * quantity
        self.transaction_history.append((sandwich_size, recipes[sandwich_size]["cost"] * quantity))
        self.customer_orders[customer_id].append((sandwich_size, recipes[sandwich_size]["cost"] * quantity))
        print(f"Your {quantity} {sandwich_size} sandwich is ready! Enjoy :) ")

    def print_report(self):
        print(f"Sandwiches sold: {self.total_sandwiches_sold}")
        print(f"Total revenue: ${self.total_revenue:.2f}")
        print(f"Bread: {self.machine_resources['bread']} slices")
        print(f"Ham: {self.machine_resources['ham']} slices")
        print(f"Cheese: {self.machine_resources['cheese']} ounces")
        print(f"Number of resupplies: {self.resupply_count}")
        print(f"Revenue of breakdown: {self.revenue_breakdown}")
        print(f"Ingredient usage: {self.ingredient_usage}")
        if self.total_sandwiches_sold > 0:
            average_revenue = self.total_revenue / self.total_sandwiches_sold
            print(f"Average revenue per sandwich sold: ${average_revenue:.2f}")
        else:
            print("No sandwich has been sold yet")
        for item, amount in self.machine_resources.items():
            if amount <= 2:
                print(f"Warning: {item} is running low")
        print("\nCustomer Order Breakdown: ")
        for customer_id, orders in self.customer_orders.items():
            if orders:
                print(f"Customer {customer_id}")
                for order in orders:
                    print(f" {order[0]} sandwich, ${order[1]:.2f}")


### Make an instance of SandwichMachine class and write the rest of the codes ###
def main():
    sandwich_machine = SandwichMachine(resources, original_resources)
    machine_on = True
    customer_id = 1

    for item, amount in sandwich_machine.machine_resources.items():
        if amount <= 2:
            print(f"Warning: {item} is running low")

    total_cost = 0
    customer_order = []

    for sandwich_size in ["small", "medium", "large"]:
        while True:
            quantity = int(input(f"How many {sandwich_size} sandwiches do you want? "))
            if quantity > 0:
                order = recipes[sandwich_size]
                total_ingredients = {item: quantity * amount for item, amount in order["ingredients"].items()}
                can_make, missing_item = sandwich_machine.check_resources(total_ingredients)
                if can_make:
                    total_cost += order["cost"] * quantity
                    customer_order.append((sandwich_size, order["ingredients"], quantity))
                    break
                else:
                    print(f"Sorry, there is not enough {missing_item} to make your sandwich")
                    reduce_quantity = input("Would you like to reduce the quantity? (yes/no): ").strip().lower()
                    if reduce_quantity == "no":
                        break
            else:
                break

    if customer_order:
        print(f"The total cost is ${total_cost:.2f}.")
        payment = sandwich_machine.process_coins()
        if sandwich_machine.transaction_result(payment, total_cost):
            for sandwich_size, ingredients, quantity in customer_order:
                sandwich_machine.make_sandwich(sandwich_size, ingredients, customer_id, quantity)

    print("Please select what to do next: ")
    next_action = input("(Report/Continue/Off): ").strip().lower()
    if next_action == "continue":
        machine_on
    elif next_action == "report":
        sandwich_machine.print_report()
    elif next_action == "off":
        machine_on = False
    else:
        print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
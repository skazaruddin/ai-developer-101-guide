# Chapter 10: Travel Assistant Agent Project

## Building a Complete AI-Powered Travel Planner

---

## Project Overview

In this capstone project, you'll build a **Virtual Travel Assistant Agent** that helps users plan their trips based on:
- Location preferences
- Budget constraints
- Number of travelers
- Travel type (adventure, relaxation, cultural, etc.)
- Real-time weather and travel advisories

This project brings together everything you've learned:
- Python programming
- API integration
- AI/LLM usage
- Agent architecture
- Memory systems
- Tool usage

---

## Features

### Core Features

1. **Personalized Itinerary Generation**
   - Creates day-by-day travel plans
   - Considers user preferences and constraints
   - Suggests activities, restaurants, and accommodations

2. **Smart Recommendations**
   - Suggests destinations based on travel type
   - Recommends alternatives based on budget
   - Adapts to group size

3. **Real-Time Information**
   - Weather forecasts and warnings
   - Travel advisories
   - Best time to visit suggestions

4. **Interactive Planning**
   - Conversational interface
   - Remembers user preferences
   - Allows itinerary modifications

### Tools Available to the Agent

| Tool | Purpose |
|------|---------|
| `search_destinations` | Find destinations matching criteria |
| `get_weather` | Get weather forecast for a location |
| `get_travel_advisory` | Check travel warnings/advisories |
| `search_flights` | Find flight options |
| `search_hotels` | Find accommodation options |
| `search_activities` | Find activities at destination |
| `calculate_budget` | Estimate trip costs |

---

## Project Structure

```
travel-assistant/
├── README.md           # This file
├── requirements.txt    # Dependencies
├── .env.example        # Environment variables template
├── main.py             # Entry point
├── agent/
│   ├── __init__.py
│   ├── travel_agent.py # Main agent class
│   ├── tools.py        # Tool definitions
│   └── prompts.py      # System prompts
├── memory/
│   ├── __init__.py
│   └── memory.py       # Memory management
├── utils/
│   ├── __init__.py
│   └── helpers.py      # Utility functions
└── data/
    └── destinations.json  # Sample destination data
```

---

## Implementation

### Step 1: Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install openai python-dotenv requests
```

### Step 2: Create .env file

```
OPENAI_API_KEY=your-openai-api-key-here
```

---

## Complete Code

### main.py

```python
"""
Travel Assistant Agent - Main Entry Point
A virtual travel planner that helps users plan their perfect trip.
"""

from dotenv import load_dotenv
from agent.travel_agent import TravelAssistant

load_dotenv()


def main():
    """Run the travel assistant."""
    print("=" * 60)
    print("  Welcome to the AI Travel Assistant!")
    print("=" * 60)
    print()
    print("I can help you plan your perfect trip. Tell me about:")
    print("- Where you'd like to go (or ask for suggestions)")
    print("- Your budget")
    print("- Number of travelers")
    print("- Type of trip (adventure, relaxation, cultural, etc.)")
    print()
    print("Type 'quit' to exit, 'new' to start a new trip plan.")
    print("-" * 60)

    assistant = TravelAssistant()

    while True:
        print()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("\nThank you for using the Travel Assistant. Have a great trip!")
            break

        if user_input.lower() == 'new':
            assistant.reset()
            print("\nStarting a new trip plan. Tell me about your ideal vacation!")
            continue

        response = assistant.chat(user_input)
        print(f"\nAssistant: {response}")


if __name__ == "__main__":
    main()
```

### agent/travel_agent.py

```python
"""
Travel Assistant Agent
Main agent class that orchestrates the travel planning process.
"""

from openai import OpenAI
import json
from typing import Optional
import os

from .tools import TravelTools
from .prompts import SYSTEM_PROMPT
from memory.memory import TravelMemory


class TravelAssistant:
    """AI-powered travel planning assistant."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = TravelTools()
        self.memory = TravelMemory()
        self.model = "gpt-4o-mini"

    def reset(self):
        """Reset the assistant for a new trip plan."""
        self.memory.clear()

    def chat(self, user_message: str) -> str:
        """Process user message and generate response."""
        # Add to conversation history
        self.memory.add_message("user", user_message)

        # Extract and remember preferences from message
        self._extract_preferences(user_message)

        # Build context
        context = self._build_context()

        # Create messages for API call
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context},
        ]
        messages.extend(self.memory.get_conversation_history())

        # Get tool definitions
        tools = self._get_tool_definitions()

        # Call the API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # Process response
        assistant_message = response.choices[0].message

        # Handle tool calls
        if assistant_message.tool_calls:
            return self._handle_tool_calls(assistant_message, messages)

        # Regular response
        response_text = assistant_message.content
        self.memory.add_message("assistant", response_text)
        return response_text

    def _extract_preferences(self, message: str):
        """Extract travel preferences from user message."""
        message_lower = message.lower()

        # Extract budget
        if "$" in message or "budget" in message_lower:
            # Simple extraction - in production, use NLP
            words = message.split()
            for i, word in enumerate(words):
                if "$" in word:
                    try:
                        amount = int(''.join(filter(str.isdigit, word)))
                        self.memory.set_preference("budget", amount)
                    except:
                        pass

        # Extract number of travelers
        for phrase in ["2 people", "two people", "couple", "just me", "solo"]:
            if phrase in message_lower:
                if "solo" in phrase or "just me" in phrase:
                    self.memory.set_preference("travelers", 1)
                elif "couple" in phrase or "2" in phrase or "two" in phrase:
                    self.memory.set_preference("travelers", 2)

        # Extract travel type
        travel_types = {
            "adventure": ["adventure", "hiking", "extreme", "thrill"],
            "relaxation": ["relax", "beach", "spa", "peaceful", "calm"],
            "cultural": ["culture", "history", "museum", "heritage", "local"],
            "romantic": ["romantic", "honeymoon", "anniversary", "couples"],
            "family": ["family", "kids", "children", "family-friendly"]
        }

        for travel_type, keywords in travel_types.items():
            if any(kw in message_lower for kw in keywords):
                self.memory.set_preference("travel_type", travel_type)
                break

        # Extract destination
        common_destinations = [
            "paris", "tokyo", "new york", "london", "rome", "barcelona",
            "bali", "thailand", "greece", "hawaii", "dubai", "sydney"
        ]
        for dest in common_destinations:
            if dest in message_lower:
                self.memory.set_preference("destination", dest.title())

    def _build_context(self) -> str:
        """Build context from memory for the system prompt."""
        prefs = self.memory.get_preferences()
        if not prefs:
            return "No preferences gathered yet."

        parts = ["Current user preferences:"]
        for key, value in prefs.items():
            parts.append(f"- {key}: {value}")

        return "\n".join(parts)

    def _get_tool_definitions(self) -> list:
        """Get OpenAI function definitions for tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_destinations",
                    "description": "Search for travel destinations based on criteria",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "travel_type": {
                                "type": "string",
                                "description": "Type of travel: adventure, relaxation, cultural, romantic, family"
                            },
                            "budget": {
                                "type": "string",
                                "description": "Budget level: budget, moderate, luxury"
                            },
                            "region": {
                                "type": "string",
                                "description": "Preferred region: europe, asia, americas, oceania, africa"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather forecast for a destination",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City or destination name"
                            },
                            "month": {
                                "type": "string",
                                "description": "Month to check weather for"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_travel_advisory",
                    "description": "Get travel advisory and safety information for a destination",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "country": {
                                "type": "string",
                                "description": "Country name"
                            }
                        },
                        "required": ["country"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_activities",
                    "description": "Search for activities and attractions at a destination",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Destination name"
                            },
                            "activity_type": {
                                "type": "string",
                                "description": "Type of activity: sightseeing, outdoor, food, nightlife, shopping"
                            }
                        },
                        "required": ["location"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "estimate_trip_cost",
                    "description": "Estimate the total cost of a trip",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "destination": {
                                "type": "string",
                                "description": "Destination city/country"
                            },
                            "duration_days": {
                                "type": "integer",
                                "description": "Number of days"
                            },
                            "travelers": {
                                "type": "integer",
                                "description": "Number of travelers"
                            },
                            "travel_style": {
                                "type": "string",
                                "description": "Travel style: budget, moderate, luxury"
                            }
                        },
                        "required": ["destination", "duration_days"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_itinerary",
                    "description": "Create a day-by-day travel itinerary",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "destination": {
                                "type": "string",
                                "description": "Destination"
                            },
                            "duration_days": {
                                "type": "integer",
                                "description": "Number of days"
                            },
                            "travel_type": {
                                "type": "string",
                                "description": "Type of trip"
                            },
                            "interests": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of interests"
                            }
                        },
                        "required": ["destination", "duration_days"]
                    }
                }
            }
        ]

    def _handle_tool_calls(self, assistant_message, messages) -> str:
        """Handle tool calls from the assistant."""
        # Add assistant message with tool calls
        messages.append(assistant_message)

        # Process each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Execute the tool
            if hasattr(self.tools, function_name):
                result = getattr(self.tools, function_name)(**arguments)
            else:
                result = f"Unknown tool: {function_name}"

            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Get final response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )

        final_response = response.choices[0].message.content
        self.memory.add_message("assistant", final_response)
        return final_response
```

### agent/tools.py

```python
"""
Travel Assistant Tools
Tools that the agent can use to gather information.
"""

import random
from datetime import datetime, timedelta


class TravelTools:
    """Collection of tools for travel planning."""

    def search_destinations(
        self,
        travel_type: str = None,
        budget: str = None,
        region: str = None
    ) -> dict:
        """Search for destinations matching criteria."""
        destinations = {
            "adventure": [
                {"name": "New Zealand", "highlights": "Bungee jumping, hiking, Lord of the Rings tours", "best_for": "Thrill seekers"},
                {"name": "Costa Rica", "highlights": "Zip-lining, surfing, volcano tours", "best_for": "Nature lovers"},
                {"name": "Nepal", "highlights": "Trekking, Everest base camp, rafting", "best_for": "Mountain enthusiasts"},
                {"name": "Iceland", "highlights": "Glaciers, northern lights, hot springs", "best_for": "Unique landscapes"}
            ],
            "relaxation": [
                {"name": "Maldives", "highlights": "Overwater bungalows, crystal waters, spa", "best_for": "Ultimate relaxation"},
                {"name": "Bali, Indonesia", "highlights": "Beaches, temples, wellness retreats", "best_for": "Mind and body"},
                {"name": "Santorini, Greece", "highlights": "Sunsets, beaches, wine tasting", "best_for": "Romantic getaways"},
                {"name": "Fiji", "highlights": "Private islands, snorkeling, local culture", "best_for": "Tropical escape"}
            ],
            "cultural": [
                {"name": "Kyoto, Japan", "highlights": "Temples, geisha districts, traditional arts", "best_for": "History buffs"},
                {"name": "Rome, Italy", "highlights": "Colosseum, Vatican, ancient history", "best_for": "History enthusiasts"},
                {"name": "Marrakech, Morocco", "highlights": "Souks, palaces, Sahara day trips", "best_for": "Exotic culture"},
                {"name": "Cusco, Peru", "highlights": "Machu Picchu, Incan heritage, Andes", "best_for": "Ancient civilizations"}
            ],
            "romantic": [
                {"name": "Paris, France", "highlights": "Eiffel Tower, Seine cruises, fine dining", "best_for": "Classic romance"},
                {"name": "Venice, Italy", "highlights": "Gondola rides, art, charming streets", "best_for": "Unique experiences"},
                {"name": "Maui, Hawaii", "highlights": "Beaches, waterfalls, sunsets", "best_for": "Natural beauty"},
                {"name": "Prague, Czech Republic", "highlights": "Castle, old town, affordable luxury", "best_for": "Fairytale setting"}
            ],
            "family": [
                {"name": "Orlando, Florida", "highlights": "Theme parks, beaches nearby, year-round sun", "best_for": "Kids of all ages"},
                {"name": "Tokyo, Japan", "highlights": "Disney, technology, safe and clean", "best_for": "Unique family experience"},
                {"name": "Barcelona, Spain", "highlights": "Beaches, Gaudi, food, culture", "best_for": "Mix of activities"},
                {"name": "London, UK", "highlights": "Museums (free!), Harry Potter, history", "best_for": "Educational fun"}
            ]
        }

        # Get matching destinations
        if travel_type and travel_type in destinations:
            results = destinations[travel_type]
        else:
            # Return mix of all
            results = []
            for dests in destinations.values():
                results.extend(random.sample(dests, min(2, len(dests))))

        return {
            "destinations": results[:5],
            "search_criteria": {
                "travel_type": travel_type,
                "budget": budget,
                "region": region
            }
        }

    def get_weather(self, location: str, month: str = None) -> dict:
        """Get weather forecast for a location."""
        # Simulated weather data
        weather_patterns = {
            "paris": {"spring": "15°C, mild", "summer": "25°C, warm", "fall": "12°C, cool", "winter": "5°C, cold"},
            "tokyo": {"spring": "18°C, cherry blossoms", "summer": "30°C, hot and humid", "fall": "20°C, pleasant", "winter": "8°C, cool"},
            "bali": {"dry": "28°C, sunny", "wet": "27°C, afternoon showers"},
            "default": {"spring": "20°C, pleasant", "summer": "28°C, warm", "fall": "18°C, mild", "winter": "10°C, cool"}
        }

        location_lower = location.lower()
        weather = weather_patterns.get(location_lower, weather_patterns["default"])

        # Determine current season/conditions
        current_month = datetime.now().month
        if 3 <= current_month <= 5:
            season = "spring"
        elif 6 <= current_month <= 8:
            season = "summer"
        elif 9 <= current_month <= 11:
            season = "fall"
        else:
            season = "winter"

        current_weather = weather.get(season, list(weather.values())[0])

        return {
            "location": location,
            "current_conditions": current_weather,
            "forecast": f"Next 7 days: Similar conditions expected",
            "best_time_to_visit": self._get_best_time(location),
            "packing_tips": self._get_packing_tips(season)
        }

    def _get_best_time(self, location: str) -> str:
        best_times = {
            "paris": "April-June or September-October",
            "tokyo": "March-May (cherry blossoms) or October-November",
            "bali": "April-October (dry season)",
            "new york": "April-June or September-November",
            "london": "May-September",
            "rome": "April-June or September-October"
        }
        return best_times.get(location.lower(), "Spring or Fall typically best")

    def _get_packing_tips(self, season: str) -> list:
        tips = {
            "spring": ["Light layers", "Rain jacket", "Comfortable walking shoes"],
            "summer": ["Light clothing", "Sunscreen", "Hat", "Sunglasses"],
            "fall": ["Layers", "Light jacket", "Umbrella"],
            "winter": ["Warm coat", "Layers", "Scarf and gloves"]
        }
        return tips.get(season, tips["spring"])

    def get_travel_advisory(self, country: str) -> dict:
        """Get travel advisory for a country."""
        # Simulated advisory data
        advisories = {
            "safe": {
                "level": "Level 1 - Exercise Normal Precautions",
                "warnings": [],
                "tips": ["Standard travel precautions apply", "Keep copies of important documents"]
            },
            "caution": {
                "level": "Level 2 - Exercise Increased Caution",
                "warnings": ["Petty crime in tourist areas", "Be aware of surroundings"],
                "tips": ["Don't display expensive items", "Use hotel safes", "Stay in well-lit areas"]
            }
        }

        # Most tourist destinations are safe
        safe_countries = ["france", "japan", "italy", "spain", "germany", "uk", "australia", "new zealand"]

        if country.lower() in safe_countries:
            advisory = advisories["safe"]
        else:
            advisory = advisories["caution"]

        return {
            "country": country,
            "advisory": advisory,
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "visa_info": f"Check visa requirements for {country} based on your nationality",
            "health_info": "Check CDC recommendations for required/recommended vaccinations"
        }

    def search_activities(
        self,
        location: str,
        activity_type: str = None
    ) -> dict:
        """Search for activities at a destination."""
        # Simulated activity database
        all_activities = {
            "paris": {
                "sightseeing": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Arc de Triomphe", "Sacré-Cœur"],
                "food": ["Seine dinner cruise", "French cooking class", "Wine tasting", "Cheese tour"],
                "outdoor": ["Luxembourg Gardens", "Bike tour", "Seine river walk", "Montmartre walking tour"]
            },
            "tokyo": {
                "sightseeing": ["Senso-ji Temple", "Tokyo Skytree", "Imperial Palace", "Shibuya Crossing"],
                "food": ["Sushi making class", "Tsukiji food tour", "Ramen tour", "Izakaya hopping"],
                "outdoor": ["Mount Fuji day trip", "Shinjuku Gyoen", "Ueno Park", "Harajuku walk"]
            },
            "default": {
                "sightseeing": ["City walking tour", "Main attractions", "Museum visits"],
                "food": ["Local food tour", "Cooking class", "Market visit"],
                "outdoor": ["Parks and gardens", "Hiking nearby", "Beach/waterfront"]
            }
        }

        location_lower = location.lower()
        activities = all_activities.get(location_lower, all_activities["default"])

        if activity_type and activity_type in activities:
            result = activities[activity_type]
        else:
            result = []
            for acts in activities.values():
                result.extend(acts[:3])

        return {
            "location": location,
            "activities": result,
            "tips": [
                "Book popular attractions in advance",
                "Consider a city pass for savings",
                "Check opening hours before visiting"
            ]
        }

    def estimate_trip_cost(
        self,
        destination: str,
        duration_days: int,
        travelers: int = 1,
        travel_style: str = "moderate"
    ) -> dict:
        """Estimate trip costs."""
        # Base daily costs by style (per person)
        daily_costs = {
            "budget": {"accommodation": 50, "food": 30, "activities": 20, "transport": 15},
            "moderate": {"accommodation": 150, "food": 60, "activities": 50, "transport": 30},
            "luxury": {"accommodation": 400, "food": 150, "activities": 100, "transport": 80}
        }

        # Destination cost multipliers
        cost_multipliers = {
            "tokyo": 1.3,
            "paris": 1.2,
            "london": 1.3,
            "new york": 1.4,
            "bali": 0.6,
            "thailand": 0.5,
            "mexico": 0.7,
            "default": 1.0
        }

        style = travel_style.lower() if travel_style else "moderate"
        costs = daily_costs.get(style, daily_costs["moderate"])
        multiplier = cost_multipliers.get(destination.lower(), 1.0)

        # Calculate costs
        daily_per_person = sum(costs.values()) * multiplier
        total_daily = daily_per_person * travelers
        total_trip = total_daily * duration_days

        # Estimate flights (rough)
        flight_estimate = 800 * travelers  # Average international flight

        return {
            "destination": destination,
            "duration": f"{duration_days} days",
            "travelers": travelers,
            "style": travel_style,
            "breakdown": {
                "flights_estimate": f"${flight_estimate:,.0f}",
                "accommodation": f"${costs['accommodation'] * multiplier * duration_days * travelers:,.0f}",
                "food": f"${costs['food'] * multiplier * duration_days * travelers:,.0f}",
                "activities": f"${costs['activities'] * multiplier * duration_days * travelers:,.0f}",
                "transport": f"${costs['transport'] * multiplier * duration_days * travelers:,.0f}"
            },
            "total_estimate": f"${total_trip + flight_estimate:,.0f}",
            "daily_average": f"${total_daily:,.0f}",
            "notes": [
                "Prices are estimates and vary by season",
                "Book in advance for better deals",
                "Consider travel insurance"
            ]
        }

    def create_itinerary(
        self,
        destination: str,
        duration_days: int,
        travel_type: str = None,
        interests: list = None
    ) -> dict:
        """Create a day-by-day itinerary."""
        # Get activities for the destination
        activities_data = self.search_activities(destination)
        available_activities = activities_data["activities"]

        itinerary = []

        for day in range(1, duration_days + 1):
            if day == 1:
                # Arrival day
                day_plan = {
                    "day": day,
                    "theme": "Arrival & Orientation",
                    "activities": [
                        "Arrive and check into hotel",
                        "Rest and freshen up",
                        "Explore the neighborhood",
                        "Welcome dinner at local restaurant"
                    ]
                }
            elif day == duration_days:
                # Departure day
                day_plan = {
                    "day": day,
                    "theme": "Departure",
                    "activities": [
                        "Pack and check out",
                        "Last-minute shopping or sightseeing",
                        "Head to airport"
                    ]
                }
            else:
                # Regular days
                theme = self._get_day_theme(day, travel_type)
                selected_activities = random.sample(
                    available_activities,
                    min(3, len(available_activities))
                )
                day_plan = {
                    "day": day,
                    "theme": theme,
                    "activities": [
                        f"Morning: {selected_activities[0] if selected_activities else 'Sightseeing'}",
                        f"Lunch: Try local cuisine",
                        f"Afternoon: {selected_activities[1] if len(selected_activities) > 1 else 'Explore'}",
                        f"Evening: {selected_activities[2] if len(selected_activities) > 2 else 'Dinner and relaxation'}"
                    ]
                }

            itinerary.append(day_plan)

        return {
            "destination": destination,
            "duration": f"{duration_days} days",
            "itinerary": itinerary,
            "tips": [
                "This is a suggested itinerary - feel free to adjust",
                "Leave room for spontaneous discoveries",
                "Book major attractions in advance"
            ]
        }

    def _get_day_theme(self, day: int, travel_type: str = None) -> str:
        """Get a theme for a day based on travel type."""
        themes = {
            "adventure": ["Active Exploration", "Outdoor Adventure", "Thrill Seeking", "Nature Day"],
            "relaxation": ["Beach & Spa", "Leisurely Morning", "Wellness Day", "Quiet Exploration"],
            "cultural": ["History & Heritage", "Art & Museums", "Local Culture", "Architecture Tour"],
            "romantic": ["Romantic Stroll", "Couples Experience", "Scenic Views", "Fine Dining Day"],
            "family": ["Fun for All Ages", "Theme Park Day", "Nature & Wildlife", "Interactive Experience"]
        }

        type_themes = themes.get(travel_type, ["Full Day Exploration", "Sightseeing", "Local Discovery"])
        return type_themes[(day - 1) % len(type_themes)]
```

### agent/prompts.py

```python
"""
System prompts for the Travel Assistant.
"""

SYSTEM_PROMPT = """You are an expert travel planning assistant with extensive knowledge of destinations worldwide.

Your role is to help users plan their perfect trip by:
1. Understanding their preferences (budget, travel style, interests)
2. Suggesting suitable destinations
3. Creating personalized itineraries
4. Providing practical travel advice

## Your Personality
- Friendly and enthusiastic about travel
- Knowledgeable but not condescending
- Practical and helpful
- Culturally sensitive

## Guidelines
- Always gather key information: destination, dates, budget, travelers, travel type
- Provide specific, actionable recommendations
- Consider weather and best times to visit
- Mention any travel advisories when relevant
- Suggest alternatives if the original plan doesn't fit constraints

## Tools Available
You have access to tools for:
- Searching destinations
- Checking weather
- Getting travel advisories
- Finding activities
- Estimating costs
- Creating itineraries

Use these tools proactively to provide accurate, helpful information.

## Response Style
- Be concise but informative
- Use bullet points for lists
- Include practical tips
- Ask clarifying questions when needed
- Summarize recommendations at the end of planning discussions
"""
```

### memory/memory.py

```python
"""
Memory management for the Travel Assistant.
"""

from datetime import datetime
from typing import Dict, List, Optional


class TravelMemory:
    """Memory system for travel planning conversations."""

    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.user_preferences: Dict = {}
        self.trip_plans: List[Dict] = []
        self.session_start = datetime.now()

    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history in OpenAI format."""
        return [
            {"role": msg["role"], "content": msg["content"]}
            for msg in self.conversation_history[-20:]  # Last 20 messages
        ]

    def set_preference(self, key: str, value):
        """Set a user preference."""
        self.user_preferences[key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }

    def get_preference(self, key: str) -> Optional[any]:
        """Get a user preference."""
        pref = self.user_preferences.get(key)
        return pref["value"] if pref else None

    def get_preferences(self) -> Dict:
        """Get all preferences."""
        return {k: v["value"] for k, v in self.user_preferences.items()}

    def save_trip_plan(self, plan: Dict):
        """Save a trip plan."""
        plan["saved_at"] = datetime.now().isoformat()
        self.trip_plans.append(plan)

    def get_trip_plans(self) -> List[Dict]:
        """Get all saved trip plans."""
        return self.trip_plans

    def clear(self):
        """Clear memory for a new session."""
        self.conversation_history = []
        self.user_preferences = {}
        self.trip_plans = []
        self.session_start = datetime.now()

    def get_context_summary(self) -> str:
        """Get a summary of the current context."""
        parts = []

        if self.user_preferences:
            parts.append("User Preferences:")
            for key, data in self.user_preferences.items():
                parts.append(f"  - {key}: {data['value']}")

        if self.trip_plans:
            parts.append(f"\nSaved Plans: {len(self.trip_plans)}")

        return "\n".join(parts) if parts else "No context yet."
```

### requirements.txt

```
openai>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0
```

---

## Running the Project

```bash
# Navigate to project directory
cd Projects/travel-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the assistant
python main.py
```

---

## Sample Conversation

```
================================================
  Welcome to the AI Travel Assistant!
================================================

I can help you plan your perfect trip. Tell me about:
- Where you'd like to go (or ask for suggestions)
- Your budget
- Number of travelers
- Type of trip (adventure, relaxation, cultural, etc.)

Type 'quit' to exit, 'new' to start a new trip plan.
------------------------------------------------------------

You: Hi! I want to plan a romantic getaway for me and my partner.
     We have about $3000 budget and want to relax but also see some
     beautiful places.
# CarWash Dar es Salaam - React Native Mobile App

A professional carwash services mobile application built with React Native and Expo, designed for Dar es Salaam, Tanzania. The app provides a Bolt-like experience for booking car wash services at your doorstep.

## 🚗 Features

### Core Functionality
- **User Authentication**: Secure login and registration with email/social media
- **Service Booking**: Easy booking of carwash services with date/time selection
- **Real-time Map Integration**: View nearby carwash service providers
- **Multiple Service Types**: Basic Wash, Premium Wash, and Full Detail services
- **Service History**: Track all your past bookings and ratings
- **User Profile Management**: Complete profile management with preferences
- **Payment Integration**: Multiple payment methods (Mobile Money, Cash, Card)
- **Rating & Reviews**: Rate services and view customer reviews

### User Experience
- **Modern UI Design**: Clean, intuitive interface similar to Bolt
- **Location Services**: GPS-based service provider matching
- **Push Notifications**: Booking confirmations and updates
- **Service Tracking**: Real-time updates on service status
- **Add-on Services**: Engine cleaning, seat conditioning, etc.
- **Special Instructions**: Custom requests for service providers

## 🛠 Tech Stack

- **Framework**: React Native with Expo
- **Navigation**: React Navigation 6
- **Maps**: React Native Maps
- **Location**: Expo Location
- **UI Components**: Custom components with Ionicons
- **Styling**: React Native StyleSheet
- **State Management**: React Hooks
- **Animations**: React Native Animated API

## 📱 App Structure

```
CarwashApp/
├── src/
│   ├── screens/
│   │   ├── WelcomeScreen.js          # App intro with animated logo
│   │   ├── LoginScreen.js            # User authentication
│   │   ├── RegisterScreen.js         # User registration
│   │   ├── HomeScreen.js             # Main dashboard with map
│   │   ├── BookingScreen.js          # Service booking flow
│   │   ├── HistoryScreen.js          # Booking history
│   │   ├── ProfileScreen.js          # User profile management
│   │   ├── ServiceDetailsScreen.js   # Detailed service info
│   │   └── BookingConfirmationScreen.js # Booking confirmation
│   ├── components/                   # Reusable components
│   ├── navigation/                   # Navigation configuration
│   ├── services/                     # API services
│   ├── utils/                        # Utility functions
│   └── assets/                       # Images and icons
├── assets/                           # Expo assets
├── App.js                           # Main app component
├── app.json                         # Expo configuration
└── package.json                     # Dependencies
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Expo CLI
- iOS Simulator / Android Emulator or physical device

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CarwashApp
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   # or
   expo start
   ```

4. **Run on device/simulator**
   - **iOS**: Press `i` or scan QR code with Camera app
   - **Android**: Press `a` or scan QR code with Expo Go app
   - **Web**: Press `w` for web version

## 📱 App Flow

### Authentication Flow
1. **Welcome Screen**: Animated intro with app branding
2. **Login/Register**: User authentication with email/social media
3. **Main App**: Access to all features after authentication

### Booking Flow
1. **Home Screen**: View map with nearby service providers
2. **Service Selection**: Choose from Basic, Premium, or Full Detail
3. **Booking Details**: Select date, time, and vehicle information
4. **Service Details**: View service inclusions and add-ons
5. **Confirmation**: Review booking and select payment method
6. **Booking Complete**: Confirmation with service provider details

### Service Types

| Service | Price (TSH) | Duration | Description |
|---------|-------------|----------|-------------|
| Basic Wash | 15,000 | 30 min | Exterior wash & dry |
| Premium Wash | 25,000 | 45 min | Interior + Exterior + Wax |
| Full Detail | 45,000 | 90 min | Complete detailing service |

### Add-on Services
- Engine Cleaning: +TSH 10,000
- Seat Conditioning: +TSH 15,000
- Odor Removal: +TSH 8,000
- Headlight Restoration: +TSH 12,000

## 🗺 Location Coverage

Currently serving **Dar es Salaam, Tanzania** with service locations including:
- Msimbazi Center
- Kariakoo Market
- Mlimani City
- And more locations across the city

## 💳 Payment Methods

- **Mobile Money**: M-Pesa, Airtel Money
- **Cash on Service**: Pay when service is completed
- **Credit/Debit Card**: Visa, Mastercard

## 📋 Configuration

### Environment Setup
The app uses Expo managed workflow with the following key configurations:

- **Location Services**: Required for finding nearby services
- **Maps Integration**: Google Maps for Android, Apple Maps for iOS
- **Push Notifications**: For booking confirmations and updates
- **Camera Access**: For profile pictures and service photos

### App Permissions
- Location access (required)
- Camera access (optional)
- Storage access (optional)
- Network access (required)

## 🔧 Development

### Key Dependencies
```json
{
  "@react-navigation/native": "Navigation framework",
  "@react-navigation/stack": "Stack navigation",
  "@react-navigation/bottom-tabs": "Tab navigation",
  "react-native-maps": "Map integration",
  "expo-location": "Location services",
  "expo-linear-gradient": "Gradient backgrounds",
  "@expo/vector-icons": "Icon library",
  "react-native-safe-area-context": "Safe area handling"
}
```

### Building for Production

1. **Expo Build**
   ```bash
   expo build:android
   expo build:ios
   ```

2. **Standalone App**
   ```bash
   expo eject  # If needed for custom native code
   ```

## 🎨 Design System

### Colors
- **Primary**: #007AFF (iOS Blue)
- **Secondary**: #0051D5 (Darker Blue)
- **Success**: #34C759 (Green)
- **Warning**: #FF9500 (Orange)
- **Error**: #FF3B30 (Red)
- **Background**: #FFFFFF (White)
- **Surface**: #F5F5F5 (Light Gray)

### Typography
- **Headers**: System font, bold (600-700)
- **Body**: System font, regular (400-500)
- **Captions**: System font, light (300-400)

## 🚀 Future Enhancements

### Planned Features
- [ ] Real-time service tracking
- [ ] In-app chat with service providers
- [ ] Loyalty program and rewards
- [ ] Subscription services
- [ ] Multi-language support (Swahili)
- [ ] Service provider app
- [ ] Advanced scheduling options
- [ ] Integration with calendar apps
- [ ] Promotional codes and discounts
- [ ] Service customization options

### Technical Improvements
- [ ] Offline support
- [ ] Performance optimizations
- [ ] Advanced animations
- [ ] Push notification enhancements
- [ ] Analytics integration
- [ ] Error tracking
- [ ] Automated testing
- [ ] Code splitting

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support and inquiries:
- Email: support@carwash-tz.com
- Phone: +255 XXX XXX XXX
- Website: www.carwash-tz.com

## 🌟 Acknowledgments

- Inspired by Bolt's user experience design
- Built for the Dar es Salaam market
- Designed with local payment methods in mind
- Focused on mobile-first experience

---

**Made with ❤️ for Dar es Salaam car owners**
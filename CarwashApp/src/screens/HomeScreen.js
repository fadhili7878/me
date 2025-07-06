import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  Dimensions,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import MapView, { Marker } from 'react-native-maps';
import * as Location from 'expo-location';
import { LinearGradient } from 'expo-linear-gradient';

const { width, height } = Dimensions.get('window');

const CARWASH_SERVICES = [
  {
    id: 1,
    name: 'Basic Wash',
    price: 'TSH 15,000',
    duration: '30 min',
    description: 'Exterior wash & dry',
    icon: 'car-outline',
    color: '#007AFF',
  },
  {
    id: 2,
    name: 'Premium Wash',
    price: 'TSH 25,000',
    duration: '45 min',
    description: 'Interior + Exterior + Wax',
    icon: 'car-sport-outline',
    color: '#FF9500',
  },
  {
    id: 3,
    name: 'Full Detail',
    price: 'TSH 45,000',
    duration: '90 min',
    description: 'Complete detailing service',
    icon: 'diamond-outline',
    color: '#34C759',
  },
];

const NEARBY_LOCATIONS = [
  {
    id: 1,
    name: 'Msimbazi Center',
    distance: '0.5 km',
    rating: 4.8,
    latitude: -6.8162,
    longitude: 39.2803,
  },
  {
    id: 2,
    name: 'Kariakoo Market',
    distance: '1.2 km',
    rating: 4.6,
    latitude: -6.8150,
    longitude: 39.2650,
  },
  {
    id: 3,
    name: 'Mlimani City',
    distance: '2.0 km',
    rating: 4.9,
    latitude: -6.7732,
    longitude: 39.2155,
  },
];

export default function HomeScreen({ navigation }) {
  const [location, setLocation] = useState(null);
  const [selectedService, setSelectedService] = useState(null);
  const [showServices, setShowServices] = useState(false);
  const [userName, setUserName] = useState('John');

  useEffect(() => {
    getCurrentLocation();
  }, []);

  const getCurrentLocation = async () => {
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        Alert.alert('Permission denied', 'Location access is required for this app');
        return;
      }

      let currentLocation = await Location.getCurrentPositionAsync({});
      setLocation({
        latitude: currentLocation.coords.latitude,
        longitude: currentLocation.coords.longitude,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      });
    } catch (error) {
      console.error('Error getting location:', error);
      // Set default location to Dar es Salaam
      setLocation({
        latitude: -6.7924,
        longitude: 39.2083,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      });
    }
  };

  const handleServiceSelect = (service) => {
    setSelectedService(service);
    navigation.navigate('ServiceDetails', { service });
  };

  const toggleServicesPanel = () => {
    setShowServices(!showServices);
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <TouchableOpacity style={styles.menuButton}>
            <Ionicons name="menu" size={24} color="#333" />
          </TouchableOpacity>
          <View style={styles.locationInfo}>
            <Text style={styles.greeting}>Hello, {userName}!</Text>
            <View style={styles.locationContainer}>
              <Ionicons name="location-outline" size={16} color="#666" />
              <Text style={styles.locationText}>Dar es Salaam, Tanzania</Text>
            </View>
          </View>
        </View>
        <TouchableOpacity style={styles.notificationButton}>
          <Ionicons name="notifications-outline" size={24} color="#333" />
          <View style={styles.notificationBadge}>
            <Text style={styles.notificationCount}>3</Text>
          </View>
        </TouchableOpacity>
      </View>

      {/* Map */}
      <View style={styles.mapContainer}>
        {location && (
          <MapView
            style={styles.map}
            initialRegion={location}
            showsUserLocation={true}
            showsMyLocationButton={true}
          >
            <Marker
              coordinate={location}
              title="Your Location"
              description="You are here"
            />
            {NEARBY_LOCATIONS.map((loc) => (
              <Marker
                key={loc.id}
                coordinate={{
                  latitude: loc.latitude,
                  longitude: loc.longitude,
                }}
                title={loc.name}
                description={`${loc.distance} away • ${loc.rating} ⭐`}
              >
                <View style={styles.carwashMarker}>
                  <Ionicons name="car-sport" size={20} color="#fff" />
                </View>
              </Marker>
            ))}
          </MapView>
        )}
        
        {/* Current Location Button */}
        <TouchableOpacity
          style={styles.currentLocationButton}
          onPress={getCurrentLocation}
        >
          <Ionicons name="locate" size={24} color="#007AFF" />
        </TouchableOpacity>
      </View>

      {/* Service Selection Panel */}
      <View style={[styles.servicePanel, showServices && styles.servicePanelExpanded]}>
        <TouchableOpacity
          style={styles.servicePanelHeader}
          onPress={toggleServicesPanel}
        >
          <View style={styles.panelHandle} />
          <Text style={styles.servicePanelTitle}>Choose Your Service</Text>
          <Ionicons 
            name={showServices ? 'chevron-down' : 'chevron-up'} 
            size={24} 
            color="#666" 
          />
        </TouchableOpacity>

        {showServices && (
          <ScrollView style={styles.servicesList} showsVerticalScrollIndicator={false}>
            {CARWASH_SERVICES.map((service) => (
              <TouchableOpacity
                key={service.id}
                style={[
                  styles.serviceItem,
                  selectedService?.id === service.id && styles.serviceItemSelected
                ]}
                onPress={() => handleServiceSelect(service)}
              >
                <View style={[styles.serviceIcon, { backgroundColor: service.color }]}>
                  <Ionicons name={service.icon} size={24} color="#fff" />
                </View>
                <View style={styles.serviceInfo}>
                  <Text style={styles.serviceName}>{service.name}</Text>
                  <Text style={styles.serviceDescription}>{service.description}</Text>
                  <View style={styles.serviceDetails}>
                    <Text style={styles.servicePrice}>{service.price}</Text>
                    <Text style={styles.serviceDuration}>• {service.duration}</Text>
                  </View>
                </View>
                <Ionicons name="chevron-forward" size={20} color="#666" />
              </TouchableOpacity>
            ))}
          </ScrollView>
        )}

        {/* Quick Book Button */}
        <View style={styles.quickBookContainer}>
          <TouchableOpacity
            style={styles.quickBookButton}
            onPress={() => navigation.navigate('Booking')}
          >
            <LinearGradient
              colors={['#007AFF', '#0051D5']}
              style={styles.quickBookGradient}
            >
              <Ionicons name="calendar" size={20} color="#fff" />
              <Text style={styles.quickBookText}>Book Service</Text>
            </LinearGradient>
          </TouchableOpacity>
        </View>
      </View>

      {/* Recent Services */}
      <View style={styles.recentSection}>
        <Text style={styles.sectionTitle}>Recent Services</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.recentList}>
          {[1, 2, 3].map((item) => (
            <TouchableOpacity key={item} style={styles.recentItem}>
              <View style={styles.recentIcon}>
                <Ionicons name="car-sport" size={20} color="#007AFF" />
              </View>
              <Text style={styles.recentText}>Premium Wash</Text>
              <Text style={styles.recentDate}>Dec 15</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  menuButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  locationInfo: {
    flex: 1,
  },
  greeting: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  locationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  locationText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  notificationButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  notificationBadge: {
    position: 'absolute',
    top: 2,
    right: 2,
    backgroundColor: '#FF3B30',
    borderRadius: 8,
    width: 16,
    height: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationCount: {
    color: '#fff',
    fontSize: 10,
    fontWeight: '600',
  },
  mapContainer: {
    flex: 1,
    position: 'relative',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  carwashMarker: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: '#fff',
  },
  currentLocationButton: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  servicePanel: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 5,
    maxHeight: height * 0.6,
  },
  servicePanelExpanded: {
    maxHeight: height * 0.8,
  },
  servicePanelHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  panelHandle: {
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#ddd',
  },
  servicePanelTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    flex: 1,
    textAlign: 'center',
  },
  servicesList: {
    flex: 1,
    paddingHorizontal: 20,
  },
  serviceItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  serviceItemSelected: {
    backgroundColor: '#F0F8FF',
  },
  serviceIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  serviceInfo: {
    flex: 1,
  },
  serviceName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  serviceDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  serviceDetails: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  servicePrice: {
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
  },
  serviceDuration: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  quickBookContainer: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
  },
  quickBookButton: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  quickBookGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
  },
  quickBookText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  recentSection: {
    position: 'absolute',
    top: 80,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    paddingVertical: 16,
    paddingHorizontal: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  recentList: {
    flexDirection: 'row',
  },
  recentItem: {
    alignItems: 'center',
    marginRight: 20,
    paddingVertical: 8,
  },
  recentIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F0F8FF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
  },
  recentText: {
    fontSize: 12,
    fontWeight: '500',
    color: '#333',
    textAlign: 'center',
  },
  recentDate: {
    fontSize: 10,
    color: '#666',
  },
});
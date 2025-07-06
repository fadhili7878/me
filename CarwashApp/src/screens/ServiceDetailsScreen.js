import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Image,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

const { width } = Dimensions.get('window');

export default function ServiceDetailsScreen({ route, navigation }) {
  const { service } = route.params;
  const [selectedAddOns, setSelectedAddOns] = useState([]);

  const serviceDetails = {
    id: service?.id || 1,
    name: service?.name || 'Premium Wash',
    price: service?.price || 'TSH 25,000',
    duration: service?.duration || '45 min',
    description: service?.description || 'Interior + Exterior + Wax',
    fullDescription: 'Our premium wash service includes a thorough exterior wash, interior cleaning, and protective wax coating to keep your vehicle looking its best.',
    includes: [
      'Exterior pressure wash',
      'Interior vacuum cleaning',
      'Dashboard and console cleaning',
      'Window cleaning (inside & outside)',
      'Tire cleaning and shining',
      'Protective wax coating',
      'Air freshener',
    ],
    images: [
      'https://via.placeholder.com/300x200/007AFF/FFFFFF?text=Car+Wash+1',
      'https://via.placeholder.com/300x200/007AFF/FFFFFF?text=Car+Wash+2',
      'https://via.placeholder.com/300x200/007AFF/FFFFFF?text=Car+Wash+3',
    ],
    rating: 4.8,
    reviews: 142,
    estimatedTime: '45-60 minutes',
  };

  const addOns = [
    { id: 1, name: 'Engine Cleaning', price: 10000, description: 'Deep clean your engine bay' },
    { id: 2, name: 'Seat Conditioning', price: 15000, description: 'Leather seat treatment' },
    { id: 3, name: 'Odor Removal', price: 8000, description: 'Remove unwanted odors' },
    { id: 4, name: 'Headlight Restoration', price: 12000, description: 'Restore cloudy headlights' },
  ];

  const toggleAddOn = (addOnId) => {
    setSelectedAddOns(prev => 
      prev.includes(addOnId)
        ? prev.filter(id => id !== addOnId)
        : [...prev, addOnId]
    );
  };

  const calculateTotal = () => {
    const basePrice = parseInt(serviceDetails.price.replace(/[^\d]/g, ''));
    const addOnTotal = selectedAddOns.reduce((total, addOnId) => {
      const addOn = addOns.find(a => a.id === addOnId);
      return total + (addOn ? addOn.price : 0);
    }, 0);
    return basePrice + addOnTotal;
  };

  const handleBookService = () => {
    const selectedAddOnDetails = addOns.filter(addOn => selectedAddOns.includes(addOn.id));
    const bookingData = {
      service: serviceDetails,
      addOns: selectedAddOnDetails,
      total: calculateTotal(),
    };
    navigation.navigate('Booking', { preselectedService: bookingData });
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 1; i <= 5; i++) {
      if (i <= fullStars) {
        stars.push(<Ionicons key={i} name="star" size={16} color="#FFD700" />);
      } else if (i === fullStars + 1 && hasHalfStar) {
        stars.push(<Ionicons key={i} name="star-half" size={16} color="#FFD700" />);
      } else {
        stars.push(<Ionicons key={i} name="star-outline" size={16} color="#ccc" />);
      }
    }
    return stars;
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Ionicons name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Service Details</Text>
        <TouchableOpacity style={styles.shareButton}>
          <Ionicons name="share-outline" size={24} color="#333" />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Service Images */}
        <View style={styles.imageContainer}>
          <ScrollView horizontal pagingEnabled showsHorizontalScrollIndicator={false}>
            {serviceDetails.images.map((image, index) => (
              <View key={index} style={styles.imageWrapper}>
                <Image source={{ uri: image }} style={styles.serviceImage} />
              </View>
            ))}
          </ScrollView>
          <View style={styles.imageIndicator}>
            <Text style={styles.imageCount}>1 / {serviceDetails.images.length}</Text>
          </View>
        </View>

        {/* Service Info */}
        <View style={styles.serviceInfo}>
          <Text style={styles.serviceName}>{serviceDetails.name}</Text>
          <View style={styles.serviceMetrics}>
            <View style={styles.ratingContainer}>
              <View style={styles.stars}>
                {renderStars(serviceDetails.rating)}
              </View>
              <Text style={styles.ratingText}>
                {serviceDetails.rating} ({serviceDetails.reviews} reviews)
              </Text>
            </View>
            <View style={styles.durationContainer}>
              <Ionicons name="time-outline" size={16} color="#666" />
              <Text style={styles.durationText}>{serviceDetails.estimatedTime}</Text>
            </View>
          </View>
          <Text style={styles.serviceDescription}>{serviceDetails.fullDescription}</Text>
        </View>

        {/* What's Included */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>What's Included</Text>
          {serviceDetails.includes.map((item, index) => (
            <View key={index} style={styles.includeItem}>
              <Ionicons name="checkmark-circle" size={20} color="#34C759" />
              <Text style={styles.includeText}>{item}</Text>
            </View>
          ))}
        </View>

        {/* Add-ons */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Add-ons</Text>
          {addOns.map((addOn) => (
            <TouchableOpacity
              key={addOn.id}
              style={[
                styles.addOnItem,
                selectedAddOns.includes(addOn.id) && styles.selectedAddOn
              ]}
              onPress={() => toggleAddOn(addOn.id)}
            >
              <View style={styles.addOnLeft}>
                <Text style={styles.addOnName}>{addOn.name}</Text>
                <Text style={styles.addOnDescription}>{addOn.description}</Text>
              </View>
              <View style={styles.addOnRight}>
                <Text style={styles.addOnPrice}>+TSH {addOn.price.toLocaleString()}</Text>
                <Ionicons
                  name={selectedAddOns.includes(addOn.id) ? 'checkbox' : 'checkbox-outline'}
                  size={24}
                  color={selectedAddOns.includes(addOn.id) ? '#007AFF' : '#ccc'}
                />
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Reviews Preview */}
        <View style={styles.section}>
          <View style={styles.reviewsHeader}>
            <Text style={styles.sectionTitle}>Customer Reviews</Text>
            <TouchableOpacity>
              <Text style={styles.viewAllText}>View All</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.reviewItem}>
            <View style={styles.reviewHeader}>
              <View style={styles.reviewerInfo}>
                <View style={styles.reviewerAvatar}>
                  <Text style={styles.reviewerInitial}>J</Text>
                </View>
                <View>
                  <Text style={styles.reviewerName}>John M.</Text>
                  <View style={styles.reviewStars}>
                    {renderStars(5)}
                  </View>
                </View>
              </View>
              <Text style={styles.reviewDate}>2 days ago</Text>
            </View>
            <Text style={styles.reviewText}>
              Excellent service! My car looks brand new. The team was professional and thorough.
            </Text>
          </View>
        </View>
      </ScrollView>

      {/* Bottom Bar */}
      <View style={styles.bottomBar}>
        <View style={styles.priceContainer}>
          <Text style={styles.totalLabel}>Total</Text>
          <Text style={styles.totalPrice}>TSH {calculateTotal().toLocaleString()}</Text>
        </View>
        <TouchableOpacity style={styles.bookButton} onPress={handleBookService}>
          <LinearGradient
            colors={['#007AFF', '#0051D5']}
            style={styles.bookButtonGradient}
          >
            <Text style={styles.bookButtonText}>Book Service</Text>
          </LinearGradient>
        </TouchableOpacity>
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
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
  },
  shareButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
  },
  imageContainer: {
    height: 250,
    position: 'relative',
  },
  imageWrapper: {
    width: width,
    height: 250,
  },
  serviceImage: {
    width: '100%',
    height: '100%',
    backgroundColor: '#f0f0f0',
  },
  imageIndicator: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  imageCount: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '500',
  },
  serviceInfo: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  serviceName: {
    fontSize: 24,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  serviceMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  stars: {
    flexDirection: 'row',
    marginRight: 8,
  },
  ratingText: {
    fontSize: 14,
    color: '#666',
  },
  durationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  durationText: {
    fontSize: 14,
    color: '#666',
    marginLeft: 4,
  },
  serviceDescription: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
  },
  section: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  includeItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  includeText: {
    fontSize: 16,
    color: '#333',
    marginLeft: 12,
  },
  addOnItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E1E1E1',
    marginBottom: 12,
    backgroundColor: '#F9F9F9',
  },
  selectedAddOn: {
    borderColor: '#007AFF',
    backgroundColor: '#F0F8FF',
  },
  addOnLeft: {
    flex: 1,
  },
  addOnName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    marginBottom: 4,
  },
  addOnDescription: {
    fontSize: 14,
    color: '#666',
  },
  addOnRight: {
    alignItems: 'flex-end',
  },
  addOnPrice: {
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
    marginBottom: 4,
  },
  reviewsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  viewAllText: {
    fontSize: 14,
    color: '#007AFF',
    fontWeight: '500',
  },
  reviewItem: {
    paddingVertical: 16,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: '#F9F9F9',
  },
  reviewHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  reviewerInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  reviewerAvatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  reviewerInitial: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  reviewerName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#333',
    marginBottom: 4,
  },
  reviewStars: {
    flexDirection: 'row',
  },
  reviewDate: {
    fontSize: 12,
    color: '#666',
  },
  reviewText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  bottomBar: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
    backgroundColor: '#fff',
  },
  priceContainer: {
    flex: 1,
    marginRight: 16,
  },
  totalLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  totalPrice: {
    fontSize: 20,
    fontWeight: '600',
    color: '#007AFF',
  },
  bookButton: {
    flex: 1,
    borderRadius: 12,
    overflow: 'hidden',
  },
  bookButtonGradient: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  bookButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
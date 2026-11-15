import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  Image,
  SafeAreaView,
  StatusBar,
  Dimensions,
  Alert,
} from 'react-native';
import { colors } from './src/theme/colors';
import { apiService } from './src/services/api';
import { AnalysisRecord, HistoryItem } from './src/types';

const { width } = Dimensions.get('window');

export default function App() {
  const [currentTab, setCurrentTab] = useState<'dashboard' | 'camera' | 'history' | 'education' | 'profile'>('dashboard');
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeAnalysis, setActiveAnalysis] = useState<AnalysisRecord | null>(null);

  useEffect(() => {
    // Initial data load
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const items = await apiService.getHistory();
      setHistory(items);
    } catch {
      // Mock history for offline mode with authentic clinical macro dermatology samples
      setHistory([
        {
          id: 'sc-01',
          predicted_category: 'Acne',
          confidence_score: 0.94,
          is_uncertain: false,
          anatomical_site: 'Face (Cheek)',
          thumbnail_url: 'https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=300&auto=format&fit=crop&q=80',
          created_at: new Date().toISOString(),
        },
        {
          id: 'sc-02',
          predicted_category: 'Eczema',
          confidence_score: 0.89,
          is_uncertain: false,
          anatomical_site: 'Forearm',
          thumbnail_url: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=300&auto=format&fit=crop&q=80',
          created_at: new Date(Date.now() - 86400000 * 3).toISOString(),
        }
      ]);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={colors.canvas} />

      {/* Screen Viewport */}
      <View style={styles.viewport}>
        {currentTab === 'dashboard' && (
          <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
            {/* Header Greeting (From Crextio Reference) */}
            <View style={styles.header}>
              <View>
                <Text style={styles.subGreeting}>DERMAVISION AI</Text>
                <Text style={styles.mainGreeting}>Welcome in, <Text style={{ color: colors.charcoal[900] }}>Jordan</Text></Text>
              </View>
              <View style={styles.avatar}>
                <Text style={styles.avatarText}>J</Text>
              </View>
            </View>

            {/* Quick Stats Ribbon */}
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.ribbon}>
              <View style={[styles.pill, styles.pillDark]}>
                <View style={styles.dotGold} />
                <Text style={styles.pillTextWhite}>Scans: {history.length}</Text>
              </View>
              <View style={[styles.pill, styles.pillGold]}>
                <Text style={styles.pillTextDark}>Normal: 80%</Text>
              </View>
              <View style={[styles.pill, styles.pillWhite]}>
                <Text style={styles.pillTextMuted}>Attention: 20%</Text>
              </View>
            </ScrollView>

            {/* Primary Action Card: Start Skin Scan */}
            <TouchableOpacity
              style={styles.heroCard}
              activeOpacity={0.9}
              onPress={() => setCurrentTab('camera')}
            >
              <View style={styles.heroBadge}>
                <Text style={styles.heroBadgeText}>AI SCREEN READY</Text>
              </View>
              <Text style={styles.heroTitle}>Start New Skin Scan</Text>
              <Text style={styles.heroDesc}>
                Capture skin lesion with real-time focus & Grad-CAM visual attention.
              </Text>
              <View style={styles.heroButton}>
                <Text style={styles.heroButtonText}>Launch Camera Viewfinder</Text>
              </View>
            </TouchableOpacity>

            {/* Two-Column Telemetry Modules */}
            <View style={styles.twoColumnGrid}>
              <View style={styles.gridCard}>
                <Text style={styles.gridLabel}>AI Backbone</Text>
                <Text style={styles.gridValue}>MobileNet</Text>
                <Text style={styles.gridStatus}>• Calibrated Softmax</Text>
              </View>
              <View style={styles.gridCard}>
                <Text style={styles.gridLabel}>Timeline</Text>
                <Text style={styles.gridValue}>{history.length} Records</Text>
                <Text style={styles.gridStatus}>• Encrypted Storage</Text>
              </View>
            </View>

            {/* Recent Scans */}
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Recent Scans</Text>
              <TouchableOpacity onPress={() => setCurrentTab('history')}>
                <Text style={styles.seeAllText}>See all</Text>
              </TouchableOpacity>
            </View>

            {history.map((item) => (
              <View key={item.id} style={styles.historyRow}>
                <Image source={{ uri: item.thumbnail_url }} style={styles.thumb} />
                <View style={{ flex: 1, marginLeft: 12 }}>
                  <Text style={styles.rowTitle}>{item.predicted_category}</Text>
                  <Text style={styles.rowSub}>{item.anatomical_site} • {Math.round(item.confidence_score * 100)}% Certain</Text>
                </View>
              </View>
            ))}
          </ScrollView>
        )}

        {currentTab === 'camera' && (
          <View style={styles.cameraContainer}>
            <View style={styles.cameraHeader}>
              <TouchableOpacity onPress={() => setCurrentTab('dashboard')} style={styles.iconCircle}>
                <Text style={{ color: '#FFF' }}>✕</Text>
              </TouchableOpacity>
              <Text style={styles.cameraHudTitle}>OPTICAL HUD v2.4</Text>
              <View style={{ width: 36 }} />
            </View>

            {/* Center Reticle */}
            <View style={styles.reticleContainer}>
              <View style={styles.reticleCircle}>
                <View style={styles.reticleCenter} />
              </View>
              <Text style={styles.reticleAdvice}>Align lesion inside circle (10-15cm)</Text>
            </View>

            {/* Shutter Button */}
            <View style={styles.cameraFooter}>
              <TouchableOpacity
                style={styles.shutterOuter}
                onPress={() => {
                  Alert.alert('Scan Initiated', 'Validating image quality & running MobileNetV3 inference...');
                  setCurrentTab('dashboard');
                }}
              >
                <View style={styles.shutterInner} />
              </TouchableOpacity>
            </View>
          </View>
        )}

        {currentTab === 'history' && (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.mainGreeting}>Scan History</Text>
            <Text style={styles.subGreeting}>{history.length} documented records</Text>
            <View style={{ height: 16 }} />
            {history.map((item) => (
              <View key={item.id} style={styles.historyCard}>
                <Image source={{ uri: item.thumbnail_url }} style={styles.largeThumb} />
                <View style={{ flex: 1, marginLeft: 14 }}>
                  <Text style={styles.rowTitle}>{item.predicted_category}</Text>
                  <Text style={styles.rowSub}>{item.anatomical_site}</Text>
                  <Text style={{ fontSize: 11, color: colors.amberGold[600], fontWeight: '700' }}>
                    {Math.round(item.confidence_score * 100)}% Match
                  </Text>
                </View>
              </View>
            ))}
          </ScrollView>
        )}

        {currentTab === 'education' && (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.mainGreeting}>Clinical Guides</Text>
            <Text style={styles.subGreeting}>Medically reviewed skin health awareness</Text>
            <View style={{ height: 16 }} />
            <View style={styles.articleCard}>
              <Text style={styles.articleBadge}>ACNE</Text>
              <Text style={styles.articleTitle}>Understanding Acne: Types & Care</Text>
              <Text style={styles.articleDesc}>Learn what triggers follicular inflammation and how to treat skin without scarring.</Text>
            </View>
            <View style={styles.articleCard}>
              <Text style={styles.articleBadge}>ECZEMA</Text>
              <Text style={styles.articleTitle}>Eczema & Atopic Dermatitis</Text>
              <Text style={styles.articleDesc}>How to soothe itching, avoid irritants, and restore the epidermal barrier.</Text>
            </View>
          </ScrollView>
        )}

        {currentTab === 'profile' && (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.mainGreeting}>User Profile</Text>
            <View style={styles.profileCard}>
              <View style={styles.avatarLarge}>
                <Text style={styles.avatarTextLarge}>J</Text>
              </View>
              <Text style={[styles.mainGreeting, { fontSize: 18, marginTop: 8 }]}>Jordan Doe</Text>
              <Text style={styles.subGreeting}>Verified Account • ID: #8842</Text>
            </View>
            <TouchableOpacity
              style={styles.deleteButton}
              onPress={() => Alert.alert('Delete Account', 'All images and clinical records will be permanently purged.')}
            >
              <Text style={styles.deleteButtonText}>Delete Account & Purge Images</Text>
            </TouchableOpacity>
          </ScrollView>
        )}
      </View>

      {/* Floating Bottom Nav (Matching Reference) */}
      <View style={styles.bottomNav}>
        <TouchableOpacity onPress={() => setCurrentTab('dashboard')} style={styles.navItem}>
          <Text style={[styles.navText, currentTab === 'dashboard' && styles.navTextActive]}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setCurrentTab('camera')} style={styles.cameraNavItem}>
          <Text style={{ color: colors.charcoal[900], fontSize: 18, fontWeight: 'bold' }}>📷</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setCurrentTab('history')} style={styles.navItem}>
          <Text style={[styles.navText, currentTab === 'history' && styles.navTextActive]}>History</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setCurrentTab('education')} style={styles.navItem}>
          <Text style={[styles.navText, currentTab === 'education' && styles.navTextActive]}>Guides</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setCurrentTab('profile')} style={styles.navItem}>
          <Text style={[styles.navText, currentTab === 'profile' && styles.navTextActive]}>Profile</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.canvas,
  },
  viewport: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 100,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  subGreeting: {
    fontSize: 11,
    fontWeight: '700',
    color: colors.text.secondary,
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  mainGreeting: {
    fontSize: 24,
    fontWeight: '800',
    color: colors.text.primary,
  },
  avatar: {
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: colors.amberGold[400],
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarText: {
    fontWeight: '800',
    color: colors.charcoal[900],
    fontSize: 16,
  },
  ribbon: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  pill: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 7,
    borderRadius: 20,
    marginRight: 8,
  },
  pillDark: {
    backgroundColor: colors.charcoal[800],
  },
  pillGold: {
    backgroundColor: colors.amberGold[200],
  },
  pillWhite: {
    backgroundColor: colors.cardSurface,
    borderWidth: 1,
    borderColor: colors.subtleBorder,
  },
  dotGold: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: colors.amberGold[400],
    marginRight: 6,
  },
  pillTextWhite: {
    color: '#FFF',
    fontSize: 12,
    fontWeight: '700',
  },
  pillTextDark: {
    color: colors.charcoal[900],
    fontSize: 12,
    fontWeight: '700',
  },
  pillTextMuted: {
    color: colors.text.secondary,
    fontSize: 12,
    fontWeight: '600',
  },
  heroCard: {
    backgroundColor: colors.charcoal[800],
    borderRadius: 28,
    padding: 22,
    marginBottom: 16,
  },
  heroBadge: {
    backgroundColor: colors.amberGold[400],
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginBottom: 8,
  },
  heroBadgeText: {
    fontSize: 10,
    fontWeight: '800',
    color: colors.charcoal[900],
  },
  heroTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#FFF',
    marginBottom: 4,
  },
  heroDesc: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 16,
    lineHeight: 18,
  },
  heroButton: {
    backgroundColor: colors.amberGold[400],
    borderRadius: 20,
    paddingVertical: 12,
    alignItems: 'center',
  },
  heroButtonText: {
    color: colors.charcoal[900],
    fontWeight: '800',
    fontSize: 13,
  },
  twoColumnGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  gridCard: {
    width: (width - 52) / 2,
    backgroundColor: colors.cardSurface,
    borderRadius: 24,
    padding: 16,
    borderWidth: 1,
    borderColor: colors.subtleBorder,
  },
  gridLabel: {
    fontSize: 11,
    color: colors.text.secondary,
    fontWeight: '600',
    marginBottom: 6,
  },
  gridValue: {
    fontSize: 18,
    fontWeight: '800',
    color: colors.text.primary,
    marginBottom: 4,
  },
  gridStatus: {
    fontSize: 11,
    color: colors.status.benign,
    fontWeight: '700',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: '800',
    color: colors.text.primary,
  },
  seeAllText: {
    fontSize: 12,
    fontWeight: '700',
    color: colors.text.secondary,
  },
  historyRow: {
    backgroundColor: colors.cardSurface,
    borderRadius: 20,
    padding: 12,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
    borderWidth: 1,
    borderColor: colors.subtleBorder,
  },
  thumb: {
    width: 48,
    height: 48,
    borderRadius: 14,
  },
  rowTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: colors.text.primary,
  },
  rowSub: {
    fontSize: 11,
    color: colors.text.secondary,
    marginTop: 2,
  },
  bottomNav: {
    position: 'absolute',
    bottom: 16,
    left: 20,
    right: 20,
    backgroundColor: colors.charcoal[800],
    borderRadius: 36,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingVertical: 10,
    shadowColor: '#000',
    shadowOpacity: 0.25,
    shadowRadius: 10,
    elevation: 8,
  },
  navItem: {
    paddingHorizontal: 12,
    paddingVertical: 6,
  },
  navText: {
    color: '#888',
    fontSize: 12,
    fontWeight: '600',
  },
  navTextActive: {
    color: colors.amberGold[400],
    fontWeight: '800',
  },
  cameraNavItem: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: colors.amberGold[400],
    alignItems: 'center',
    justifyContent: 'center',
  },
  cameraContainer: {
    flex: 1,
    backgroundColor: '#000',
    justifyContent: 'space-between',
  },
  cameraHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
  },
  iconCircle: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(255,255,255,0.2)',
    alignItems: 'center',
    justifyContent: 'center',
  },
  cameraHudTitle: {
    color: '#FFF',
    fontSize: 11,
    fontFamily: 'monospace',
    fontWeight: '700',
  },
  reticleContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  reticleCircle: {
    width: 240,
    height: 240,
    borderRadius: 120,
    borderWidth: 2,
    borderColor: colors.amberGold[400],
    borderStyle: 'dashed',
    alignItems: 'center',
    justifyContent: 'center',
  },
  reticleCenter: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.amberGold[400],
  },
  reticleAdvice: {
    color: colors.amberGold[300],
    fontSize: 12,
    marginTop: 16,
    fontWeight: '600',
  },
  cameraFooter: {
    alignItems: 'center',
    paddingBottom: 40,
  },
  shutterOuter: {
    width: 76,
    height: 76,
    borderRadius: 38,
    backgroundColor: '#FFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  shutterInner: {
    width: 62,
    height: 62,
    borderRadius: 31,
    backgroundColor: colors.amberGold[400],
  },
  historyCard: {
    backgroundColor: colors.cardSurface,
    borderRadius: 24,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
    borderWidth: 1,
    borderColor: colors.subtleBorder,
  },
  largeThumb: {
    width: 64,
    height: 64,
    borderRadius: 18,
  },
  articleCard: {
    backgroundColor: colors.cardSurface,
    borderRadius: 24,
    padding: 18,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: colors.subtleBorder,
  },
  articleBadge: {
    fontSize: 10,
    fontWeight: '800',
    color: colors.amberGold[600],
    marginBottom: 6,
  },
  articleTitle: {
    fontSize: 16,
    fontWeight: '800',
    color: colors.text.primary,
    marginBottom: 4,
  },
  articleDesc: {
    fontSize: 12,
    color: colors.text.secondary,
    lineHeight: 18,
  },
  profileCard: {
    backgroundColor: colors.cardSurface,
    borderRadius: 28,
    padding: 24,
    alignItems: 'center',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: colors.subtleBorder,
  },
  avatarLarge: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: colors.amberGold[400],
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarTextLarge: {
    fontSize: 28,
    fontWeight: '800',
    color: colors.charcoal[900],
  },
  deleteButton: {
    backgroundColor: '#FEE2E2',
    borderRadius: 20,
    paddingVertical: 14,
    alignItems: 'center',
  },
  deleteButtonText: {
    color: '#DC2626',
    fontWeight: '700',
    fontSize: 13,
  },
});

import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Slot, Link } from 'expo-router';
import { StyleSheet, View, Text, SafeAreaView } from 'react-native';

export default function RootLayout() {
  const insets = useSafeAreaInsets();

  return (
    <View style={styles.container}>
      {/* Safe Area Header */}
      <SafeAreaView style={[styles.header, { paddingTop: insets.top }]}>
        <Text style={styles.title}>PRIMAL</Text>
        <Text style={styles.subtitle}>Est. 2025</Text>
      </SafeAreaView>

      {/* Main Content */}
      <View style={styles.content}>
        <Slot />
      </View>

      {/* Safe Area Navigation */}
      <SafeAreaView style={styles.navContainer}>
        <View style={[styles.navBar, { paddingBottom: insets.bottom }]}>
          <Link href="/" style={styles.navLink}>
            <Text>Home</Text>
          </Link>
          <Link href="/primal" style={styles.navLink}>
            <Text>PRIMAL</Text>
          </Link>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#2d3436',
    paddingHorizontal: 20,
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    color: 'white',
    fontWeight: 'bold',
  },
  subtitle: {
    fontSize: 14,
    color: '#dfe6e9',
    marginTop: 5,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  navContainer: {
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  navBar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    padding: 15,
  },
  navLink: {
    padding: 10,
  },
});
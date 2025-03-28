import { StyleSheet, View, Text } from 'react-native';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.welcome}>Welcome to Our Bookstore! 📚</Text>
      <Text style={styles.description}>
        Discover thousands of academic books
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  welcome: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#2d3436',
    marginBottom: 15,
    textAlign: 'center',
  },
  description: {
    fontSize: 18,
    color: '#636e72',
    textAlign: 'center',
    paddingHorizontal: 30,
  },
});
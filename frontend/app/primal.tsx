import { StyleSheet, View, Text } from 'react-native';

export default function PrimalScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>PRIMAL</Text>
      <Text style={styles.text}>
        Explore our selection of amazing books 🗿
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
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2d3436',
    marginBottom: 15,
  },
  text: {
    fontSize: 18,
    color: '#636e72',
  },
});
import 'dart:async';
import 'dart:math' as math;

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _timeString = '';
  String _dateString = '';
  late Timer _timer;

  @override
  void initState() {
    super.initState();
    _updateTime();
    _timer = Timer.periodic(const Duration(seconds: 1), (Timer t) => _updateTime());
  }

  void _updateTime() {
    final DateTime now = DateTime.now();
    setState(() {
      _timeString = DateFormat('hh:mm a').format(now);
      _dateString = DateFormat('EEEE, d MMMM yyyy').format(now);
    });
  }

  List<Color> _getGradientColors() {
    final DateTime now = DateTime.now();
    final double timeDecimal = now.hour + (now.minute / 60.0);

    final Map<double, List<Color>> colorStops = <double, List<Color>>{
      0.0: <Color>[const Color(0xFF0D1424), const Color(0xFF131B32)],
      4.0: <Color>[const Color(0xFF0D1424), const Color(0xFF1B2345)],
      6.0: <Color>[const Color(0xFF3A3853), const Color(0xFFE48B6B)],
      8.0: <Color>[const Color(0xFF5AB0E2), const Color(0xFFA5D8F3)],
      12.0: <Color>[const Color(0xFF4A90E2), const Color(0xFF8ED6F3)],
      13.0: <Color>[const Color(0xFF357ABD), const Color(0xFF6FB3E0)],
      17.0: <Color>[const Color(0xFFF5A623), const Color(0xFFFFC96B)],
      18.5: <Color>[const Color(0xFFD94A5C), const Color(0xFFF39C12)],
      20.0: <Color>[const Color(0xFF1E3A5F), const Color(0xFF4A4E8F)],
      22.0: <Color>[const Color(0xFF0D1424), const Color(0xFF131B32)],
      24.0: <Color>[const Color(0xFF0D1424), const Color(0xFF131B32)],
    };

    final List<double> sortedTimes = colorStops.keys.toList()..sort();

    double lowerTime = 0.0;
    double upperTime = 24.0;
    late List<Color> lowerColors;
    late List<Color> upperColors;

    for (final double time in sortedTimes) {
      if (time <= timeDecimal) {
        lowerTime = time;
        lowerColors = colorStops[time]!;
      }
      if (time > timeDecimal) {
        upperTime = time;
        upperColors = colorStops[time]!;
        break;
      }
    }

    double factor = 0.0;
    if (upperTime != lowerTime) {
      factor = (timeDecimal - lowerTime) / (upperTime - lowerTime);
      factor = math.sin(factor * math.pi / 2);
    }

    return <Color>[
      Color.lerp(lowerColors[0], upperColors[0], factor)!,
      Color.lerp(lowerColors[1], upperColors[1], factor)!,
    ];
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AnimatedContainer(
        duration: const Duration(seconds: 1),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: _getGradientColors(),
          ),
        ),
        child: SafeArea(
          child: Stack(
            children: <Widget>[
              Positioned(
                top: 16,
                left: 16,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Text(
                      _timeString,
                      style: const TextStyle(
                        fontFamily: 'ShareTechMono',
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        shadows: <Shadow>[
                          Shadow(blurRadius: 8.0, color: Colors.black54, offset: Offset(1.0, 1.0)),
                        ],
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      _dateString,
                      style: const TextStyle(
                        fontFamily: 'ShareTechMono',
                        color: Colors.white,
                        fontSize: 13,
                        fontWeight: FontWeight.w300,
                        shadows: <Shadow>[
                          Shadow(blurRadius: 5.0, color: Colors.black45, offset: Offset(1.0, 1.0)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

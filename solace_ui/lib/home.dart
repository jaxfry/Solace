import 'dart:async';
import 'dart:convert';
import 'dart:math' as math;
import 'dart:ui';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

import 'card_widget.dart';

// Configuration for API
class LifeLogConfig {
  static String apiBaseUrl = 'http://192.168.1.75:8000'; // (My LifeLog API server running on a pi)
  static String username =
      'admin'; // Replace with your username and pass that you set up in LifeLog
  static String password = 'admin123';
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with TickerProviderStateMixin {
  String _timeString = '';
  String _dateString = '';
  late Timer _systemClockTimer;
  late PageController _pageController;
  Timer? _cardScrollTimer;
  Timer? _inactivityTimer;
  int _currentPage = 1000;
  bool _isBedtime = false;

  late AnimationController _bedtimeController;
  late List<AnimationController> _cardControllers;
  late List<Animation<Offset>> _cardAnimations;
  late List<Animation<double>> _cardOpacityAnimations;
  late List<Animation<double>> _cardBlurAnimations;

  String? _summary;

  Future<String?> _getJwtToken(String username, String password) async {
    final http.Response response = await http.post(
      Uri.parse('${LifeLogConfig.apiBaseUrl}/api/v1/auth/token'),
      headers: <String, String>{'Content-Type': 'application/json'},
      body: jsonEncode(<String, String>{'username': username, 'password': password}),
    );
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body) as Map<String, dynamic>;
      return data['access_token'] as String?;
    }
    return null;
  }

  Future<Map<String, dynamic>?> _fetchDailySummaryApi(String date, String jwt) async {
    final http.Response response = await http.get(
      Uri.parse('${LifeLogConfig.apiBaseUrl}/api/v1/day/$date'),
      headers: <String, String>{'Authorization': 'Bearer $jwt'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    }
    return null;
  }

  Future<void> _fetchSummary() async {
    setState(() {
      _summary = null;
    });
    try {
      final String? jwt = await _getJwtToken(LifeLogConfig.username, LifeLogConfig.password);
      if (jwt == null) {
        setState(() {
          _summary = 'Failed to authenticate.';
        });
        return;
      }
      final DateTime today = DateTime.now();
      final String dateStr = DateFormat('yyyy-MM-dd').format(today);
      final Map<String, dynamic>? summaryData = await _fetchDailySummaryApi(dateStr, jwt);
      setState(() {
        _summary = summaryData?['summary']?['summary']?.toString() ?? 'No summary available.';
      });
    } catch (e) {
      setState(() {
        _summary = 'Error fetching summary.';
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _pageController = PageController(initialPage: _currentPage, viewportFraction: 0.8);
    _updateTime();

    _bedtimeController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );

    _cardControllers = List.generate(1, (int index) {
      return AnimationController(duration: const Duration(milliseconds: 800), vsync: this);
    });

    _cardAnimations = List.generate(1, (int index) {
      final double delay = index * 0.15;
      return Tween<Offset>(begin: Offset.zero, end: const Offset(0, 2.5)).animate(
        CurvedAnimation(
          parent: _cardControllers[index],
          curve: Interval(delay, 1.0, curve: Curves.easeInExpo),
        ),
      );
    });

    _cardOpacityAnimations = List.generate(1, (int index) {
      final double delay = index * 0.15;
      return Tween<double>(begin: 1.0, end: 0.0).animate(
        CurvedAnimation(
          parent: _cardControllers[index],
          curve: Interval(delay, 0.8, curve: Curves.easeInQuad),
        ),
      );
    });

    _cardBlurAnimations = List.generate(1, (int index) {
      final double delay = index * 0.15;
      return Tween<double>(begin: 0.0, end: 8.0).animate(
        CurvedAnimation(
          parent: _cardControllers[index],
          curve: Interval(delay, 1.0, curve: Curves.easeInQuad),
        ),
      );
    });

    _systemClockTimer = Timer.periodic(const Duration(seconds: 1), (Timer t) => _updateTime());
    _startAutoScroll();
    _fetchSummary();
  }

  void _startAutoScroll() {
    _cardScrollTimer?.cancel();
    _cardScrollTimer = Timer.periodic(const Duration(seconds: 15), (Timer timer) {
      _currentPage++;
      _pageController.animateToPage(
        _currentPage,
        duration: const Duration(milliseconds: 450),
        curve: Curves.easeInOut,
      );
    });
  }

  void _stopAutoScroll() {
    _cardScrollTimer?.cancel();
  }

  void _handleUserInteraction() {
    _stopAutoScroll();
    _inactivityTimer?.cancel();
    _inactivityTimer = Timer(const Duration(seconds: 30), () {
      _startAutoScroll();
    });
  }

  void _updateTime() {
    final DateTime now = DateTime.now();
    setState(() {
      _timeString = DateFormat('HH:mm').format(now);
      _dateString = DateFormat('EEEE, d MMMM yyyy').format(now);
      if (now.hour == 22 && !_isBedtime) {
        _isBedtime = true;
        _stopAutoScroll();
        _startBedtimeAnimation();
      }
    });
  }

  void _startBedtimeAnimation() {
    for (int i = 0; i < _cardControllers.length; i++) {
      _cardControllers[i].forward();
    }
  }

  void _reverseBedtimeAnimation() {
    for (int i = 0; i < _cardControllers.length; i++) {
      _cardControllers[i].reverse();
    }
  }

  void _toggleBedtime() {
    setState(() {
      _isBedtime = !_isBedtime;
      if (_isBedtime) {
        _stopAutoScroll();
        _startBedtimeAnimation();
      } else {
        _startAutoScroll();
        _reverseBedtimeAnimation();
      }
    });
  }

  List<Color> _getGradientColors() {
    if (_isBedtime) {
      return <Color>[const Color(0xFF0A0F1C), const Color(0xFF1A1F2E)];
    }
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
    _systemClockTimer.cancel();
    _cardScrollTimer?.cancel();
    _inactivityTimer?.cancel();
    _pageController.dispose();
    _bedtimeController.dispose();
    for (final AnimationController controller in _cardControllers) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const Duration duration = Duration(milliseconds: 1500);
    const Cubic curve = Curves.easeInOut;

    final List<Widget> cards = <Widget>[
      CardWidget(
        title: 'LifeLog Summary',
        child: _summary == null
            ? const Center(child: CircularProgressIndicator())
            : Text(_summary!, style: const TextStyle(color: Colors.white, fontSize: 18)),
      ),
    ];

    return Scaffold(
      body: AnimatedContainer(
        duration: duration,
        curve: curve,
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
              if (!_isBedtime)
                Padding(
                  padding: const EdgeInsets.only(top: 100.0),
                  child: Listener(
                    onPointerDown: (_) => _handleUserInteraction(),
                    child: PageView.builder(
                      controller: _pageController,
                      onPageChanged: (int page) {
                        setState(() {
                          _currentPage = page;
                        });
                      },
                      itemBuilder: (BuildContext context, int index) {
                        final int cardIndex = index % cards.length;
                        return AnimatedBuilder(
                          animation: _cardControllers[cardIndex],
                          builder: (BuildContext context, Widget? child) {
                            return Transform.translate(
                              offset:
                                  _cardAnimations[cardIndex].value *
                                  MediaQuery.of(context).size.height,
                              child: Opacity(
                                opacity: _cardOpacityAnimations[cardIndex].value,
                                child: ImageFiltered(
                                  imageFilter: ImageFilter.blur(
                                    sigmaX: _cardBlurAnimations[cardIndex].value,
                                    sigmaY: _cardBlurAnimations[cardIndex].value,
                                  ),
                                  child: cards[cardIndex],
                                ),
                              ),
                            );
                          },
                        );
                      },
                    ),
                  ),
                ),
              AnimatedAlign(
                duration: duration,
                curve: curve,
                alignment: _isBedtime ? Alignment.center : Alignment.topLeft,
                child: AnimatedContainer(
                  duration: duration,
                  curve: curve,
                  padding: EdgeInsets.all(_isBedtime ? 32.0 : 16.0),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: _isBedtime
                        ? CrossAxisAlignment.center
                        : CrossAxisAlignment.start,
                    children: <Widget>[
                      AnimatedDefaultTextStyle(
                        duration: duration,
                        curve: curve,
                        style: TextStyle(
                          fontFamily: 'ShareTechMono',
                          color: Colors.white.withOpacity(_isBedtime ? 0.9 : 1.0),
                          fontSize: _isBedtime ? 120 : 28,
                          fontWeight: _isBedtime ? FontWeight.w300 : FontWeight.bold,
                          letterSpacing: _isBedtime ? 8.0 : 1.0,
                          height: _isBedtime ? 0.9 : 1.0,
                          shadows: _isBedtime
                              ? <Shadow>[
                                  const Shadow(
                                    blurRadius: 20.0,
                                    color: Colors.black26,
                                    offset: Offset(2.0, 2.0),
                                  ),
                                ]
                              : const <Shadow>[
                                  Shadow(
                                    blurRadius: 8.0,
                                    color: Colors.black54,
                                    offset: Offset(1.0, 1.0),
                                  ),
                                ],
                        ),
                        child: Text(_timeString),
                      ),
                      AnimatedContainer(
                        duration: duration,
                        curve: curve,
                        height: _isBedtime ? 16 : 2,
                      ),
                      AnimatedDefaultTextStyle(
                        duration: duration,
                        curve: curve,
                        style: TextStyle(
                          fontFamily: 'ShareTechMono',
                          color: Colors.white.withOpacity(_isBedtime ? 0.6 : 1.0),
                          fontSize: _isBedtime ? 24 : 13,
                          fontWeight: FontWeight.w300,
                          letterSpacing: _isBedtime ? 2.0 : 0.5,
                          shadows: _isBedtime
                              ? <Shadow>[
                                  const Shadow(
                                    blurRadius: 12.0,
                                    color: Colors.black26,
                                    offset: Offset(1.0, 1.0),
                                  ),
                                ]
                              : const <Shadow>[
                                  Shadow(
                                    blurRadius: 5.0,
                                    color: Colors.black45,
                                    offset: Offset(1.0, 1.0),
                                  ),
                                ],
                        ),
                        child: Text(_dateString),
                      ),
                    ],
                  ),
                ),
              ),
              Positioned(
                top: 0,
                right: 0,
                child: SafeArea(
                  child: IconButton(
                    icon: Icon(
                      _isBedtime ? Icons.wb_sunny_outlined : Icons.bedtime_outlined,
                      color: Colors.white.withOpacity(0.9),
                      size: 28,
                    ),
                    onPressed: _toggleBedtime,
                    tooltip: 'Toggle Bedtime Mode',
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

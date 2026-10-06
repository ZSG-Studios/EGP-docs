.. _doc_egp_helper_reference:

Networking helper API
=====================

These declarations are generated from EGP's shipped helper sources. Install them
with ``install_egp_net_helpers.py`` before using the high-level APIs. Native
classes are documented separately in the :ref:`class reference <doc_class_reference>`.

For behavior, ownership, limits and errors, see :doc:`networking_reference`.

GDScript
--------

EGPNet
~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/gdscript/egp_net.gd>`__

.. code-block:: gdscript

    func configure(options: Dictionary = {}) -> Error
    func host(port: int = 10515, bind_address: String = "0.0.0.0") -> Error
    func join(address: String, port: int = 10515) -> Error
    func join_token(client_id: int, token: PackedByteArray, bind_address: String = "0.0.0.0") -> Error
    func issue_token(client_id: int, public_address: String) -> Dictionary
    func set_entity_visible(entity: int, peer_id: int, visible: bool) -> Error
    func poll() -> Error
    func stop() -> void
    func close() -> void
    func is_server() -> bool
    func get_state() -> String
    func get_statistics() -> Dictionary
    func get_tick_rate() -> int
    func get_simulation_fingerprint() -> String
    func get_peers() -> Array
    func disconnect_peer(peer_id: int) -> Error
    func spawn(kind: int, state: Dictionary = {}, authority_peer: int = -1) -> int
    func update_entity(entity: int, state: Dictionary) -> Error
    func despawn(entity: int) -> Error
    func get_entities() -> Array
    func get_entity(entity: int) -> Dictionary
    func register_scene(kind: int, scene: PackedScene, parent: Node) -> Error
    func register_message(message: StringName, handler: Callable, allowed_sender: Sender = Sender.BOTH) -> Error
    func unregister_message(message: StringName) -> void
    func send_message(peer_id: int, message: StringName, arguments: Array = []) -> Error
    func broadcast_message(message: StringName, arguments: Array = []) -> Error
    func send_input(entity: int, input: Dictionary) -> Error
    func send_packet(peer_id: int, payload: PackedByteArray, channel: int = 0, delivery: Delivery = Delivery.RELIABLE_ORDERED) -> Error
    func broadcast_packet(payload: PackedByteArray, channel: int = 0, delivery: Delivery = Delivery.RELIABLE_ORDERED) -> Error

Signals:

.. code-block:: gdscript

    signal state_changed(state: String)
    signal peer_connected(peer_id: int)
    signal peer_disconnected(peer_id: int)
    signal entity_spawned(entity: int, kind: int, state: Dictionary)
    signal entity_changed(entity: int, state: Dictionary)
    signal entity_despawned(entity: int)
    signal message_received(peer_id: int, message: StringName, arguments: Array)
    signal input_received(peer_id: int, entity: int, input: Dictionary)
    signal packet_received(peer_id: int, payload: PackedByteArray, channel: int, delivery: int)
    signal diagnostic(message: String)
    signal simulation_tick(tick: int, server: bool)

EGPNetBox3D
~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/gdscript/egp_net_box3d.gd>`__

.. code-block:: gdscript

    func attach(net: Node, world: RefCounted) -> Error
    func track(entity: int, body_id: int = 0) -> Error
    func untrack(entity: int) -> void
    func detach() -> void

Signals:

.. code-block:: gdscript

    signal before_step(tick: int)
    signal after_step(tick: int)
    signal failed(error: Error)

EGPNetEntity2D
~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/gdscript/egp_net_entity_2d.gd>`__

.. code-block:: gdscript

    func apply_network_state(state: Dictionary) -> void

Signals:

.. code-block:: gdscript

    signal state_applied(state: Dictionary)

EGPNetEntity3D
~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/gdscript/egp_net_entity_3d.gd>`__

.. code-block:: gdscript

    func apply_network_state(state: Dictionary) -> void

Signals:

.. code-block:: gdscript

    signal state_applied(state: Dictionary)

EGPNetPrediction
~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/gdscript/egp_net_prediction.gd>`__

.. code-block:: gdscript

    func configure(capture: Callable, restore: Callable, simulate: Callable, initial_tick: int = 0, max_ticks: int = 128, max_state_bytes: int = 65536, max_history_bytes: int = 8388608) -> Error
    func predict(tick: int, input: PackedByteArray) -> Error
    func reconcile(acknowledged_tick: int, authoritative_state: PackedByteArray) -> Error
    func reset(tick: int, state: PackedByteArray) -> Error
    func get_pending_ticks() -> int
    func get_history_bytes() -> int

Signals:

.. code-block:: gdscript

    signal corrected(acknowledged_tick: int, replayed_inputs: int)
    signal resync_required(error: Error)

C#
--

Use ``EGP.Networking``. Public declarations below retain overloads,
default arguments, events and property accessors; method bodies are omitted.

EGP.Networking.Delivery
~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public enum Delivery { ReliableOrdered = 2, Unreliable = 4 }

EGP.Networking.Sender
~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public enum Sender { Server = 1, Client = 2, Both = 3 }

EGP.Networking.NetOptions
~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public sealed class NetOptions {
        public int TickRate { get; set; } = 60;
        public int MaxPlayers { get; set; } = 32;
        public int MaxEntities { get; set; } = 1024;
        public int MessagesPerSecond { get; set; } = 1000;
        public int BytesPerSecond { get; set; } = 4 * 1024 * 1024;
        public int TimeoutSeconds { get; set; } = 5;
        public int TokenLifetimeSeconds { get; set; } = 30;
        public string GameProtocol { get; set; } = "egp-game-v1";
        public string SimulationFingerprint { get; set; } = "script-state-v1";
        public bool AllowInsecureLoopback { get; set; }
        public byte[]? PrivateKey { get; set; }
        public float SimulatedLoss { get; set; }
        public float SimulatedLatencyMs { get; set; }
        public float SimulatedJitterMs { get; set; }
        public Dictionary ToDictionary();
    }

EGP.Networking.TokenResult
~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public readonly record struct TokenResult(Error Error, byte[] Token) {

    }

EGP.Networking.SpawnResult
~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public readonly record struct SpawnResult(Error Error, long Entity);

EGP.Networking.PeerInfo
~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public readonly record struct PeerInfo(long PeerId, long ClientId, float PingMs);

EGP.Networking.RawEntity
~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public readonly record struct RawEntity(long Entity, int Kind, long AuthorityPeer, long Revision, long Tick, byte[] State);

EGP.Networking.NetSession
~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public sealed class NetSession : IDisposable {
        public GodotObject Native { get; }
        public event Action<string>? StateChanged;
        public event Action<long>? PeerConnected;
        public event Action<long>? PeerDisconnected;
        public event Action<long, byte[]>? ApplicationReceived;
        public event Action<long, byte[], int, Delivery>? PacketReceived;
        public event Action<long, bool>? SimulationTick;
        public event Action<string>? Diagnostic;
        public NetSession();
        public Error Configure(NetOptions? options = null);
        public Error Configure(Dictionary options);
        public Error Listen(int port = 10515, string bindAddress = "0.0.0.0");
        public Error ConnectLoopback(string address, int port = 10515);
        public Error ConnectToken(long clientId, byte[] token, string bindAddress = "0.0.0.0");
        public TokenResult IssueToken(long clientId, string publicAddress);
        public Error Poll();
        public void Stop();
        public void Close();
        public string State { get; }
        public string Fingerprint { get; }
        public Dictionary Statistics { get; }
        public Variant Command(StringName operation, Dictionary? arguments = null);
        public Error SendApplication(long peer, byte[] payload);
        public Error SendPacket(long peer, byte[] payload, int channel = 0, Delivery delivery = Delivery.ReliableOrdered);
        public SpawnResult Spawn(int kind, byte[] state, long authorityPeer = -1);
        public Error UpdateEntity(long entity, byte[] state);
        public Error Despawn(long entity);
        public Error SetEntityVisible(long entity, long peer, bool visible);
        public Error DisconnectPeer(long peer);
        public PeerInfo[] GetPeers();
        public RawEntity[] GetEntities();
        public void Dispose();
    }

EGP.Networking.NetBox3D
~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetBox3D.cs>`__

.. code-block:: csharp

    public sealed class NetBox3D : IDisposable {
        public GodotObject Native { get; }
        public event Action<long>? BeforeStep;
        public event Action<long>? AfterStep;
        public event Action<Error>? Failed;
        public NetBox3D();
        public Error Attach(NetNode net, GodotObject world);
        public Error Track(long entity, long bodyId = 0);
        public void Untrack(long entity);
        public void Detach();
        public void Dispose();
    }

EGP.Networking.NetEntity2D
~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetEntity2D.cs>`__

.. code-block:: csharp

    public partial class NetEntity2D : Node2D {
        public Dictionary NetworkState { get; set; }
        public event Action<Dictionary>? StateApplied;
        public void apply_network_state(Dictionary state);
        public void ApplyNetworkState(Dictionary state);
        public override void _Process(double delta);
    }

EGP.Networking.NetEntity3D
~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetEntity3D.cs>`__

.. code-block:: csharp

    public partial class NetEntity3D : Node3D {
        public Dictionary NetworkState { get; set; }
        public event Action<Dictionary>? StateApplied;
        public void apply_network_state(Dictionary state);
        public void ApplyNetworkState(Dictionary state);
        public override void _Process(double delta);
    }

EGP.Networking.NetNode
~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetNode.cs>`__

.. code-block:: csharp

    public partial class NetNode : Node {
        public event Action<string>? StateChanged;
        public event Action<long>? PeerConnected;
        public event Action<long>? PeerDisconnected;
        public event Action<long, int, Dictionary>? EntitySpawned;
        public event Action<long, Dictionary>? EntityChanged;
        public event Action<long>? EntityDespawned;
        public event Action<long, StringName, Array>? MessageReceived;
        public event Action<long, long, Dictionary>? InputReceived;
        public event Action<long, byte[], int, Delivery>? PacketReceived;
        public event Action<long, bool>? SimulationTick;
        public event Action<string>? Diagnostic;
        public Node Bridge { get; }
        public override void _ExitTree();
        public Error Configure(NetOptions? options = null);
        public Error Configure(Dictionary options);
        public Error Host(int port = 10515, string bindAddress = "0.0.0.0");
        public Error JoinLoopback(string address, int port = 10515);
        public Error JoinToken(long clientId, byte[] token, string bindAddress = "0.0.0.0");
        public TokenResult IssueToken(long clientId, string publicAddress);
        public Error Poll();
        public void Stop();
        public void Close();
        public bool IsServer { get; }
        public string State { get; }
        public Dictionary Statistics { get; }
        public int TickRate { get; }
        public string SimulationFingerprint { get; }
        public GodotObject? NativeSession { get; }
        public Array GetPeers();
        public long Spawn(int kind, Dictionary? state = null, long authorityPeer = -1);
        public Error UpdateEntity(long entity, Dictionary state);
        public Error Despawn(long entity);
        public Error SetEntityVisible(long entity, long peer, bool visible);
        public Array GetEntities();
        public Dictionary GetEntity(long entity);
        public Error RegisterScene(int kind, PackedScene scene, Node parent);
        public Error RegisterMessage(StringName name, Callable handler, Sender sender = Sender.Both);
        public void UnregisterMessage(StringName name);
        public Error SendMessage(long peer, StringName name, Array? arguments = null);
        public Error BroadcastMessage(StringName name, Array? arguments = null);
        public Error SendInput(long entity, Dictionary input);
        public Error SendPacket(long peer, byte[] payload, int channel = 0, Delivery delivery = Delivery.ReliableOrdered);
        public Error BroadcastPacket(byte[] payload, int channel = 0, Delivery delivery = Delivery.ReliableOrdered);
        public Error DisconnectPeer(long peer);
    }

EGP.Networking.NetPrediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/csharp/NetPrediction.cs>`__

.. code-block:: csharp

    public sealed class NetPrediction : IDisposable {
        public GodotObject Native { get; }
        public event Action<long, int>? Corrected;
        public event Action<Error>? ResyncRequired;
        public NetPrediction();
        public Error Configure(Func<byte[]> capture, Func<byte[], Error> restore, Func<long, byte[], bool, Error> simulate, long initialTick = 0, int maxTicks = 128, int maxStateBytes = 65536, int maxHistoryBytes = 8388608);
        public Error Predict(long tick, byte[] input);
        public Error Reconcile(long acknowledgedTick, byte[] state);
        public Error Reset(long tick, byte[] state);
        public int PendingTicks { get; }
        public int HistoryBytes { get; }
        public void Dispose();
    }

C++
---

Include ``addons/egp_net/cpp/egp_net.hpp`` and use ``egp::networking``.
Godot types are used throughout. Public declarations omit inline bodies and
private fields. Keep wrappers alive for callbacks, and construct, call and
destroy them on the same Godot thread.

egp::networking::Delivery
~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    enum class Delivery : int { ReliableOrdered = 2, Unreliable = 4 };

egp::networking::Sender
~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    enum class Sender : int { Server = 1, Client = 2, Both = 3 };

egp::networking::Options
~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    struct Options {
        int tick_rate = 60, max_players = 32, max_entities = 1024;
        int messages_per_second = 1000, bytes_per_second = 4 * 1024 * 1024;
        int timeout_seconds = 5, token_lifetime_seconds = 30;
        String game_protocol = "egp-game-v1", simulation_fingerprint = "script-state-v1";
        bool allow_insecure_loopback = false;
        PackedByteArray private_key;
        float simulated_loss = 0, simulated_latency_ms = 0, simulated_jitter_ms = 0;
        Dictionary dictionary() const;
    };

egp::networking::TokenResult
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    struct TokenResult {
        Error error = ERR_UNCONFIGURED;
        PackedByteArray token;
        static TokenResult read(const Dictionary &d);
    };

egp::networking::SpawnResult
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    struct SpawnResult {
        Error error;
        int64_t entity;
    };

egp::networking::Session
~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    class Session {
    public:
        Session();
        ~Session();
        Session(const Session &) = delete;
        Session &operator=(const Session &) = delete;
        Ref<RefCounted> native() const;
        bool available() const;
        Error configure(const Options &options = {});
        Error configure(const Dictionary &options);
        Error listen(int port = 10515, const String &bind = "0.0.0.0");
        Error connect_loopback(const String &address, int port = 10515);
        Error connect_token(int64_t client, const PackedByteArray &token, const String &bind = "0.0.0.0");
        TokenResult issue_token(int64_t client, const String &address);
        Error poll();
        void stop();
        void close();
        String state() const;
        String fingerprint() const;
        Dictionary statistics() const;
        Variant command(const StringName &operation, const Dictionary &args = {});
        Error send_application(int64_t peer, const PackedByteArray &data);
        Error send_packet(int64_t peer, const PackedByteArray &data, int channel = 0, Delivery delivery = Delivery::ReliableOrdered);
        SpawnResult spawn(int kind, const PackedByteArray &state, int64_t authority = -1);
        Error update_entity(int64_t entity, const PackedByteArray &state);
        Error despawn(int64_t entity);
        Error set_entity_visible(int64_t entity, int64_t peer, bool visible);
        Error disconnect_peer(int64_t peer);
        Array peers();
        Array entities();
        Error connect(const StringName &signal, const Callable &callback);
        void disconnect(const StringName &signal, const Callable &callback);
    };

egp::networking::Net
~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    class Net {
    public:
        explicit Net(Node &parent);
        Net(const Net &) = delete;
        Net &operator=(const Net &) = delete;
        ~Net();
        Node *bridge() const;
        bool available() const;
        Ref<RefCounted> native_session() const;
        void set_auto_poll(bool enabled);
        Error configure(const Options &options = {});
        Error configure(const Dictionary &options);
        Error host(int port = 10515, const String &bind = "0.0.0.0");
        Error join_loopback(const String &address, int port = 10515);
        Error join_token(int64_t client, const PackedByteArray &token, const String &bind = "0.0.0.0");
        TokenResult issue_token(int64_t client, const String &address);
        Error poll();
        void stop();
        void close();
        bool is_server() const;
        String state() const;
        int tick_rate() const;
        String simulation_fingerprint() const;
        Dictionary statistics() const;
        Array peers() const;
        int64_t spawn(int kind, const Dictionary &state = {}, int64_t authority = -1);
        Error update_entity(int64_t entity, const Dictionary &state);
        Error despawn(int64_t entity);
        Error set_entity_visible(int64_t entity, int64_t peer, bool visible);
        Array entities() const;
        Dictionary entity(int64_t handle) const;
        Error register_scene(int kind, const Ref<PackedScene> &scene, Node *parent);
        Error register_message(const StringName &name, const Callable &handler, Sender sender = Sender::Both);
        void unregister_message(const StringName &name);
        Error send_message(int64_t peer, const StringName &name, const Array &arguments = {});
        Error broadcast_message(const StringName &name, const Array &arguments = {});
        Error send_input(int64_t entity, const Dictionary &input);
        Error send_packet(int64_t peer, const PackedByteArray &data, int channel = 0, Delivery delivery = Delivery::ReliableOrdered);
        Error broadcast_packet(const PackedByteArray &data, int channel = 0, Delivery delivery = Delivery::ReliableOrdered);
        Error disconnect_peer(int64_t peer);
        Error connect(const StringName &signal, const Callable &callback);
    };

egp::networking::Prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    class Prediction {
    public:
        Prediction();
        Prediction(const Prediction &) = delete;
        Prediction &operator=(const Prediction &) = delete;
        Ref<RefCounted> native() const;
        Error configure(const Callable &capture, const Callable &restore, const Callable &simulate, int64_t initial_tick = 0, int max_ticks = 128, int max_state_bytes = 65536, int max_history_bytes = 8388608);
        Error predict(int64_t tick, const PackedByteArray &input);
        Error reconcile(int64_t ack, const PackedByteArray &state);
        Error reset(int64_t tick, const PackedByteArray &state);
        int pending_ticks() const;
        int history_bytes() const;
    };

egp::networking::Box3D
~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    class Box3D {
    public:
        Box3D();
        ~Box3D();
        Box3D(const Box3D &) = delete;
        Box3D &operator=(const Box3D &) = delete;
        Ref<RefCounted> native() const;
        Error attach(Net &net, const Ref<RefCounted> &world);
        Error track(int64_t entity, int64_t body_id = 0);
        void untrack(int64_t entity);
        void detach();
    };

egp::networking::EntityPresentation3D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    class EntityPresentation3D {
    public:
        double smoothing_speed = 15.0;
        explicit EntityPresentation3D(Node3D &node);
        Dictionary state() const;
        void apply(const Dictionary &state);
        void process(double delta);
    };

egp::networking::EntityPresentation2D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/3cbba2e8d28e4f9f7666d06064ab537abbd5c4f4/modules/egp_net/cpp/egp_net.hpp>`__

.. code-block:: cpp

    class EntityPresentation2D {
    public:
        double smoothing_speed = 15.0;
        explicit EntityPresentation2D(Node2D &node);
        Dictionary state() const;
        void apply(const Dictionary &state);
        void process(double delta);
    };

Standalone native servers instead include ``modules/egp_net/net_core.h``
and use ``egp::net::Session`` without the GDScript codec. See
:doc:`networking_reference` for its distinct API contract.

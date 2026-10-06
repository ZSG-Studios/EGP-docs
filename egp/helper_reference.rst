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

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/gdscript/egp_net.gd>`__

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

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/gdscript/egp_net_box3d.gd>`__

.. code-block:: gdscript

    func attach(net: Node, world: RefCounted) -> Error
    func track(entity: int) -> Error
    func untrack(entity: int) -> void
    func detach() -> void

Signals:

.. code-block:: gdscript

    signal before_step(tick: int)
    signal after_step(tick: int)
    signal failed(error: Error)

EGPNetEntity2D
~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/gdscript/egp_net_entity_2d.gd>`__

.. code-block:: gdscript

    func apply_network_state(state: Dictionary) -> void

Signals:

.. code-block:: gdscript

    signal state_applied(state: Dictionary)

EGPNetEntity3D
~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/gdscript/egp_net_entity_3d.gd>`__

.. code-block:: gdscript

    func apply_network_state(state: Dictionary) -> void

Signals:

.. code-block:: gdscript

    signal state_applied(state: Dictionary)

EGPNetPrediction
~~~~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/gdscript/egp_net_prediction.gd>`__

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

Use the ``EGP.Networking`` namespace. The source files below declare the typed
options, events, results, ownership and disposal contracts.

NetApi
~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/csharp/NetApi.cs>`__

.. code-block:: csharp

    public int TickRate;
    public int MaxPlayers;
    public int MaxEntities;
    public int MessagesPerSecond;
    public int BytesPerSecond;
    public int TimeoutSeconds;
    public int TokenLifetimeSeconds;
    public string GameProtocol;
    public string SimulationFingerprint;
    public bool AllowInsecureLoopback;
    public byte[]? PrivateKey;
    public float SimulatedLoss;
    public float SimulatedLatencyMs;
    public float SimulatedJitterMs;
    public Dictionary ToDictionary();
    public readonly record struct TokenResult(Error Error, byte[] Token);
    public readonly record struct SpawnResult(Error Error, long Entity);
    public readonly record struct PeerInfo(long PeerId, long ClientId, float PingMs);
    public readonly record struct RawEntity(long Entity, int Kind, long AuthorityPeer, long Revision, long Tick, byte[] State);
    public void Dispose();
    public GodotObject Native;
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
    public string State;
    public string Fingerprint;
    public Dictionary Statistics;
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

NetBox3D
~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/csharp/NetBox3D.cs>`__

.. code-block:: csharp

    public GodotObject Native;
    public event Action<long>? BeforeStep;
    public event Action<long>? AfterStep;
    public event Action<Error>? Failed;
    public NetBox3D();
    public Error Attach(NetNode net, GodotObject world);
    public Error Track(long entity);
    public void Untrack(long entity);
    public void Detach();
    public void Dispose();

NetEntity2D
~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/csharp/NetEntity2D.cs>`__

.. code-block:: csharp

    public Dictionary NetworkState;
    public event Action<Dictionary>? StateApplied;
    public void apply_network_state(Dictionary state);
    public void ApplyNetworkState(Dictionary state);
    public override void _Process(double delta);

NetEntity3D
~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/csharp/NetEntity3D.cs>`__

.. code-block:: csharp

    public Dictionary NetworkState;
    public event Action<Dictionary>? StateApplied;
    public void apply_network_state(Dictionary state);
    public void ApplyNetworkState(Dictionary state);
    public override void _Process(double delta);

NetNode
~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/csharp/NetNode.cs>`__

.. code-block:: csharp

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
    public Node Bridge;
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
    public bool IsServer;
    public string State;
    public Dictionary Statistics;
    public int TickRate;
    public string SimulationFingerprint;
    public GodotObject? NativeSession;
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

NetPrediction
~~~~~~~~~~~~~

`Source <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/csharp/NetPrediction.cs>`__

.. code-block:: csharp

    public GodotObject Native;
    public event Action<long, int>? Corrected;
    public event Action<Error>? ResyncRequired;
    public NetPrediction();
    public Error Configure(Func<byte[]> capture, Func<byte[], Error> restore, Func<long, byte[], bool, Error> simulate,;
    public Error Predict(long tick, byte[] input);
    public Error Reconcile(long acknowledgedTick, byte[] state);
    public Error Reset(long tick, byte[] state);
    public int PendingTicks;
    public int HistoryBytes;
    public void Dispose();

C++
---

Include ``addons/egp_net/cpp/egp_net.hpp`` and use ``egp::networking``.
The header declares ``Options``, ``Session``, ``Net``, ``Prediction``,
``Box3D``, and 2D/3D presentation helpers. Keep wrappers alive for their
callbacks; perform calls and destruction on the constructing Godot thread.

`Complete C++ declarations <https://github.com/ZSG-Studios/EGP/blob/f31110a3d2396869741c604ed525cb1ef4801a95/modules/egp_net/cpp/egp_net.hpp>`__

Standalone native servers instead include ``modules/egp_net/net_core.h`` and
use ``egp::net::Session``. This API does not require the GDScript codec.
